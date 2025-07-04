import requests
import json
import os

# Base URL for your Flask API
BASE_URL = "http://localhost:5000"

def test_salary_prediction():
    """Test Salary Prediction API"""
    url = f"{BASE_URL}/predict_salary"
    payload = {
        "education": "PhD",
        "experience": 5,
        "location": "Rural",
        "job_title": "Director",
        "age": 32,
        "gender": "Female"
    }
    
    try:
        response = requests.post(url, json=payload)
        print("\n💰 Salary Prediction Test:")
        print("Status Code:", response.status_code)
        print("Response:", response.json())
    except Exception as e:
        print("Error testing salary prediction:", str(e))

def test_startup_prediction():
    """Test Startup Success Prediction API"""
    url = f"{BASE_URL}/predict_startup"
    
    # Your exact example input
    payload = {
        "age_first_funding_year": 2.0,
        "age_last_funding_year": 6.0,
        "relationships": 3,
        "funding_rounds": 4,
        "funding_total_usd": 15000000,
        "milestones": 2,
        "is_CA": 1,
        "is_NY": 0,
        "is_MA": 0,
        "is_TX": 0,
        "is_otherstate": 0,
        "is_software": 1,
        "is_web": 1,
        "is_mobile": 0,
        "is_enterprise": 0,
        "is_advertising": 0,
        "is_gamesvideo": 0,
        "is_ecommerce": 1,
        "is_biotech": 0,
        "is_consulting": 0,
        "is_othercategory": 0,
        "has_VC": 1,
        "has_angel": 1,
        "has_roundA": 1,
        "has_roundB": 0,
        "has_roundC": 0,
        "has_roundD": 0,
        "avg_participants": 1.5,
        "is_top500": 1,
        "labels": 1,
        "category_code": 0,
        "state_code": 0
    }
    
    try:
        response = requests.post(url, json=payload)
        print("\n🚀 Startup Prediction Test:")
        print("Status Code:", response.status_code)
        print("Response:", response.json())
        
        if response.status_code == 400:
            print("⚠️ Missing Features:", response.json().get('error', ''))
            
    except Exception as e:
        print("Error testing startup prediction:", str(e))

def test_job_recommendations():
    """Test Job Recommendation API"""
    url = f"{BASE_URL}/recommend_jobs"
    payload = {
        "query": "Machine learning engineer with Python and AWS experience",
        "top_n": 3
    }
    
    try:
        response = requests.post(url, json=payload)
        print("\n👥 Job Recommendations Test:")
        print("Status Code:", response.status_code)
        print("Number of recommendations:", len(response.json().get('recommendations', [])))
    except Exception as e:
        print("Error testing job recommendations:", str(e))

if __name__ == "__main__":
    print("🧪 Starting API Tests...")
    
    # Verify required files exist
    required_files = [
        'salary_prediction_model.pkl',
        'education_encoder.pkl',
        'location_encoder.pkl',
        'job_encoder.pkl',
        'gender_encoder.pkl',
        'startups_success_model.pkl',
        'startups_label_encoders.pkl',
        'startups_feature_names.pkl',
        'tfidf_vectorizer.pkl',
        'count_vectorizer.pkl',
        'tfidf_job_matrix.pkl',
        'count_job_matrix.pkl',
        'bert_job_embeddings.npy',
        'sampled_jobs.csv'
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print("\n❌ Missing model files:")
        for f in missing_files:
            print(f" - {f}")
        print("Please ensure all model files are in the current directory.")
    else:
        test_salary_prediction()
        test_startup_prediction()
        test_job_recommendations()
    
    print("✅ Tests completed!")