from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import nltk
import re
import os
import json

# Initialize Flask app
app = Flask(__name__)

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load startup model
try:
    model = joblib.load('dt_deployment/decision_tree_model.joblib')
    feature_names = joblib.load('dt_deployment/feature_names.joblib')
except Exception as e:
    print(f"Error loading startup model: {str(e)}")
    model = None
    feature_names = []

# Load job recommendation model
class ModelRegistry:
    def __init__(self):
        try:
            self.tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
            self.count_vectorizer = joblib.load('count_vectorizer.pkl')
            self.tfidf_job_matrix = joblib.load('tfidf_job_matrix.pkl')
            self.count_job_matrix = joblib.load('count_job_matrix.pkl')       
            self.bert_job_embeddings = np.load('bert_job_embeddings.npy')
            self.jobs_df = pd.read_csv('sampled_jobs.csv')
            self.stop_words = set(nltk.corpus.stopwords.words('english'))
            self.bert_model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"Model loading error: {str(e)}")
            raise

model_registry = ModelRegistry()

def preprocess_text(text):
    """Preprocess input text for job recommendation"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = nltk.word_tokenize(text)
    return ' '.join([t for t in tokens if t not in model_registry.stop_words])

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Salary Prediction
@app.route('/predict_salary', methods=['POST'])
def predict_salary():
    try:
        data = request.get_json()
        return jsonify({'predicted_salary': 120000})  # Placeholder
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Startup Prediction
@app.route('/predict_startup', methods=['POST'])
def predict_startup():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        missing_features = [feat for feat in feature_names if feat not in data]
        if missing_features:
            return jsonify({
                "error": f"Missing required features: {', '.join(missing_features)}",
                "expected_features": feature_names
            }), 400
        
        input_df = pd.DataFrame([data], columns=feature_names)
        prediction = model.predict(input_df)[0].item()
        status = "acquired" if prediction == 0 else "closed"
        confidence = 0.87  # Placeholder
        return jsonify({
            "prediction": status,
            "confidence": confidence,
            "status_code": prediction
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Job Recommendations
@app.route('/recommend_jobs', methods=['POST'])
def recommend_jobs():
    try:
        data = request.get_json()
        query = data['query']
        top_n = int(data.get('top_n', 3))
        
        processed_query = preprocess_text(query)
        tfidf_query = model_registry.tfidf_vectorizer.transform([processed_query])
        tfidf_scores = cosine_similarity(tfidf_query, model_registry.tfidf_job_matrix).flatten()
        count_query = model_registry.count_vectorizer.transform([processed_query])
        count_scores = cosine_similarity(count_query, model_registry.count_job_matrix).flatten()
        bert_embedding = model_registry.bert_model.encode([processed_query])
        bert_scores = cosine_similarity(bert_embedding, model_registry.bert_job_embeddings).flatten()
        
        combined_scores = (tfidf_scores + count_scores + bert_scores) / 3
        top_indices = np.argsort(combined_scores)[-top_n:][::-1]
        recommendations = model_registry.jobs_df.iloc[top_indices][['title', 'company_name', 'description']].to_dict('records')
        
        return jsonify({'recommendations': recommendations})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)