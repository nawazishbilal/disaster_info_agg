from flask import Blueprint, request, jsonify, render_template
from db import db
from models import DisasterReport
import xgboost as xgb
import requests, feedparser, os, joblib
from dotenv import load_dotenv
from twitter_api import fetch_disaster_tweets
from datetime import datetime

load_dotenv()  # Load API keys from .env

weather_bp = Blueprint("weather", __name__)
disaster_bp = Blueprint('disaster_bp', __name__)

MODEL_PATH = "disaster_model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"

if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
else:
    model, vectorizer = None, None

USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
NOMINATIM_API_URL = "https://nominatim.openstreetmap.org/search"
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

@disaster_bp.route("/")
def home():
    return render_template("index.html")

# New routes for rendering separate pages
@disaster_bp.route("/earthquakes_page")
def earthquakes_page():
    return render_template("earthquakes.html")

@disaster_bp.route("/weather_page")
def weather_page():
    return render_template("weather.html")

@disaster_bp.route("/tweets_page")
def tweets_page():
    return render_template("tweets_classify.html")

def get_coordinates(location):
    """Convert a location name into latitude and longitude using Nominatim API."""
    headers = {
        "User-Agent": "DisasterInfoApp/1.0 (nawazishbilal@gmail.com)"  # Replace with your actual email
    }
    params = {"q": location, "format": "json", "limit": 1}
    response = requests.get(NOMINATIM_API_URL, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
        else:
            return None, None  # No results found
    else:
        return None, None  # API request failed
    

# locations = ["Los Angeles", "New York", "Tokyo", "London"]
# for loc in locations:
#     lat, lon = get_coordinates(loc)
#     print(f"{loc} -> Lat: {lat}, Lon: {lon}")

@disaster_bp.route("/earthquakes", methods=["GET"])
def get_earthquakes():
    """Fetch earthquake data from USGS API with limited filters."""
    
    location = request.args.get("location","")  # User enters city/state/country
    # print(f"Received Location: {location}")  # Debugging line
    min_magnitude = request.args.get("minmagnitude", 4.5)
    max_magnitude = request.args.get("maxmagnitude")
    limit = request.args.get("limit", 10)
    orderby = request.args.get("orderby", "time")  # Default: order by latest earthquakes

    # Convert location name to coordinates if provided
    latitude, longitude = None, None
    if location:
        latitude, longitude = get_coordinates(location)
        # print(f"Resolved Coordinates: {latitude}, {longitude}")  # Debugging line
        if not latitude or not longitude:
            # print(f"USGS Response: {data}")  # Debugging line
            return jsonify({"error": "Invalid location name"}), 400

    params = {
        "format": "geojson",
        "limit": limit,
        "minmagnitude": min_magnitude,
        "maxmagnitude": max_magnitude,
        "latitude": latitude,
        "longitude": longitude,
        "maxradiuskm": 300,  # Fixed radius of 50km
        "orderby": orderby,
    }

    # Remove empty values from params
    params = {key: value for key, value in params.items() if value is not None}

    response = requests.get(USGS_API_URL, params=params)
    # print(f"USGS API Request: {response.url}")  # Debugging Line
    # print(f"USGS API Status Code: {response.status_code}")  # Debugging Line
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch earthquake data"}), 500

    data = response.json()
    earthquakes = []
    
    for feature in data.get("features", []):
        properties = feature["properties"]
        geometry = feature["geometry"]

        earthquakes.append({
            "magnitude": properties["mag"],
            "place": properties["place"],
            "time": properties["time"],
            "longitude": geometry["coordinates"][0],
            "latitude": geometry["coordinates"][1],
            "depth": geometry["coordinates"][2]
        })
    
    return jsonify({"earthquakes": earthquakes})


@disaster_bp.route("/alerts", methods=["GET"])
def alerts_page():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if start_date and end_date:
        # Fetch and filter alerts based on date
        GDACS_URL = "https://www.gdacs.org/xml/rss.xml"
        feed = feedparser.parse(GDACS_URL)

        alerts = []
        for entry in feed.entries:
            published_date = entry.published  # Ensure this format is parseable
            if start_date <= published_date <= end_date:
                alerts.append({
                    "title": entry.title,
                    "summary": entry.summary,
                    "link": entry.link,
                    "published": entry.published
                })
        
        return jsonify({"gdacs_alerts": alerts})

    return render_template("alerts.html")


@disaster_bp.route("/gdacs", methods=["GET"])
def get_gdacs_alerts():
    """Fetches real-time disaster alerts from GDACS RSS feed."""
    GDACS_URL = "https://www.gdacs.org/xml/rss.xml"
    
    # Parse the RSS feed
    feed = feedparser.parse(GDACS_URL)

    # Get disaster type filter from query params (optional)
    disaster_type = request.args.get("type", "").lower()
    location_filter = request.args.get("location", "").lower()
    start_date = request.args.get("start_date", None)
    end_date = request.args.get("end_date", None)

    # Convert start and end dates to datetime objects
    date_format = "%Y-%m-%d"  # This expects "2025-03-25"
    start_date_obj = datetime.strptime(start_date, date_format) if start_date else None
    end_date_obj = datetime.strptime(end_date, date_format) if end_date else None
    
    # Extract relevant disaster info
    alerts = []
    for entry in feed.entries:
        title_lower = entry.title.lower()  # Convert to lowercase for case-insensitive matching
        summary_lower = entry.summary.lower()

        # Convert entry.published to datetime format
        entry_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")

        # Apply date filtering
        if start_date_obj and entry_date < start_date_obj:
            continue
        if end_date_obj and entry_date > end_date_obj:
            continue

        ## Apply type filter
        if disaster_type and disaster_type not in title_lower:
            continue  # Skip this entry if it doesn't match the filter

        # Apply location filter (checks both title & summary)
        if location_filter and (location_filter not in title_lower and location_filter not in summary_lower):
            continue  # Skip if location doesn't match

        # # Convert published date to datetime object
        # try:
        #     alert_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
        # except ValueError:
        #     continue  # Skip if date parsing fails

        # # Apply date filtering
        # if start_date and end_date:
        #     start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        #     end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

        #     if not (start_date_obj <= alert_date <= end_date_obj):
        #         continue  # Skip if not in range

        alerts.append({
            "title": entry.title,
            "summary": entry.summary,
            "link": entry.link,
            "published": entry.published
        })
    
    return jsonify({"gdacs_alerts": alerts})



@weather_bp.route("/weather", methods=["GET"])
def get_weather_alerts():
    """Fetches real-time weather alerts using OpenWeather API."""
    location = request.args.get("location")  # e.g., "New York"
    
    if not location:
        return jsonify({"error": "Please provide a location"}), 400

    # Convert location to latitude & longitude
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={OPENWEATHER_API_KEY}"
    geo_response = requests.get(geocode_url).json()

    if not geo_response or "lat" not in geo_response[0] or "lon" not in geo_response[0]:
        return jsonify({"error": "Invalid location name or missing data from API"}), 400

    lat, lon = geo_response[0]["lat"], geo_response[0]["lon"]

    # Fetch weather alerts for this location
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    weather_response = requests.get(weather_url).json()

    if "cod" in weather_response and weather_response["cod"] != 200:
        return jsonify({"error": "Failed to fetch weather data"}), 500

    # Extract relevant details
    weather_data = {
        "location": location,
        "latitude": lat,   # ✅ Include coordinates
        "longitude": lon,  # ✅ Include coordinates
        "temperature": weather_response["main"]["temp"],
        "weather": weather_response["weather"][0]["description"],
        "humidity": weather_response["main"]["humidity"],
        "wind_speed": weather_response["wind"]["speed"]
    }
    #print("Geocode API Response:", geo_response)  # Debugging
    return jsonify({"weather_alerts": weather_data})



@disaster_bp.route("/tweets", methods=["GET"])
def get_tweets():
    keyword = request.args.get("keyword", "earthquake")  # Default keyword
    count = request.args.get("count", 5)

    try:
        count = int(count)
    except ValueError:
        return jsonify({"error": "Invalid count parameter"}), 400

    tweets = fetch_disaster_tweets(keyword, count)
    return jsonify(tweets)

@disaster_bp.route('/debug_vectorizer', methods=['GET'])
def debug_vectorizer():
    sample_text = ["Flood in California"]
    transformed_sample = vectorizer.transform(sample_text)
    return jsonify({"vectorized_shape": transformed_sample.shape[1]})



@disaster_bp.route('/predict', methods=['POST'])
def predict():
    if not model or not vectorizer:
        return jsonify({"error": "Model or vectorizer not found!"}), 500
    
    data = request.json
    tweet = data.get("tweet", "")

    if not tweet:
        return jsonify({"error": "No tweet provided!"}), 400

    # Transform tweet using the saved vectorizer
    transformed_tweet = vectorizer.transform([tweet])

    # Convert to DMatrix for XGBoost
    dmatrix_tweet = xgb.DMatrix(transformed_tweet)

    # Make prediction
    raw_prediction = model.predict(dmatrix_tweet)
    print("Raw Prediction:", raw_prediction)  # Debugging line

    # Check if we need to adjust the threshold
    prediction = 1 if raw_prediction[0] > 0.475 else 0  
    print("Processed Prediction:", prediction)  # Debugging line

    label = "Disaster-related" if prediction == 1 else "Not disaster-related"
    
    return jsonify({"tweet": tweet, "label": label, "raw_score": float(raw_prediction[0])})