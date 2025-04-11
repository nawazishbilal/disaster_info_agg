import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Load Bearer Token from environment variable
#BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAITb0AEAAAAAaWbdj8svoGZQ6xEGR%2B%2BUgUNE9eA%3DmXFvAwshCEM4dvMautSxPtQvUehzFHoG95xw8SEenVhUbVfCi9"

def fetch_disaster_tweets(keyword="earthquake", count=5):
    url = f"https://api.twitter.com/2/tweets/search/recent?query={keyword}&max_results={count}"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        tweets = response.json()
        return tweets.get("data", [])  # Return tweets if found
    else:
        return {"error": f"Failed to fetch tweets, status: {response.status_code}"}
