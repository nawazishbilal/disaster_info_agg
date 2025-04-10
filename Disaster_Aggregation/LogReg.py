import pandas as pd
import numpy as np
import re
import string
import nltk
import pickle
from flask import Flask, request, jsonify
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import xgboost as xgb

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

# Load the dataset
file_path = "tweets.csv"
df = pd.read_csv(file_path)

# Initialize stopwords and lemmatizer
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Preprocessing function
def clean_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'http\S+|www\S+', '', text)  # Remove URLs
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words])  # Remove stopwords & lemmatize
    return text

df['cleaned_text'] = df['text'].apply(clean_text)

# Splitting data
X = df['cleaned_text']
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TF-IDF Vectorization with unigrams and bigrams
vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1,2))
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Save vectorizer for deployment
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

# Compute scale_pos_weight to handle class imbalance
pos_weight = sum(y_train == 0) / sum(y_train == 1) * 0.9  # Slightly reduce scale_pos_weight

# Train XGBoost model with optimized hyperparameters
dmatrix_train = xgb.DMatrix(X_train_tfidf, label=y_train)
dmatrix_test = xgb.DMatrix(X_test_tfidf, label=y_test)

params = {
    'objective': 'binary:logistic',
    'eval_metric': 'logloss',
    'use_label_encoder': False,
    'random_state': 42,
    'scale_pos_weight': pos_weight,  # Adjusted class imbalance weight
    'eta': 0.08,  # Restored for stability
    'max_depth': 5,  # Increased for better learning
    'subsample': 1.0,  # Use full data per tree
    'colsample_bytree': 1.0,  # Use all features per tree
    'lambda': 1,  # L2 regularization to reduce overfitting
    'alpha': 0.5,  # L1 regularization to encourage sparsity
    'min_child_weight': 1  # Allow even more splits
}

model = xgb.train(params, dmatrix_train, num_boost_round=1000)  # Kept boosting rounds at 1000

# Save trained model
model.save_model("xgboost_model.json")

# Flask API for deployment
app = Flask(__name__)

@app2.route('/predict', methods=['POST'])
def predict():
    data = request.json
    if 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = clean_text(data['text'])
    
    # Load vectorizer
    with open("vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    text_tfidf = vectorizer.transform([text])
    
    # Load model
    dmatrix = xgb.DMatrix(text_tfidf)
    prediction_proba = model.predict(dmatrix)[0]
    prediction = int(prediction_proba > 0.5)
    
    return jsonify({'text': data['text'], 'prediction': prediction, 'probability': float(prediction_proba)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
