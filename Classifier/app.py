from flask import Flask, request, jsonify, render_template
import joblib
import os
import xgboost as xgb

app = Flask(__name__)

# Load the model and vectorizer
MODEL_PATH = "disaster_model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"

if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
else:
    model, vectorizer = None, None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
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


@app.route('/debug_vectorizer', methods=['GET'])
def debug_vectorizer():
    sample_text = ["Flood in California"]
    transformed_sample = vectorizer.transform(sample_text)
    return jsonify({"vectorized_shape": transformed_sample.shape[1]})

if __name__ == '__main__':
    app.run(debug=True)
