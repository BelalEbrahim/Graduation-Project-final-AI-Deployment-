import requests
import json
import time

def run_test():
    url = "http://localhost:5000/predict_startup"
    
    # Fallback test data (matches your example format)
    fallback_data = {
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

    # Try to load from data.json first
    try:
        with open('data.json') as f:
            print("Using data from data.json")
            test_data = json.load(f)
    except FileNotFoundError:
        print("data.json not found. Using fallback data.")
        test_data = fallback_data
    except json.JSONDecodeError:
        print("Invalid JSON in data.json. Using fallback data.")
        test_data = fallback_data

    try:
        # Send POST request
        print("Sending prediction request...")
        response = requests.post(url, json=test_data, timeout=5)
        
        # Print response
        print("\n🚀 Startup Prediction Result:")
        print("Status Code:", response.status_code)
        print("Response:", json.dumps(response.json(), indent=2))
        return 0  # Success
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error")
        print("Error: Flask server not running. Start it with 'python app.py'")
        return 1
    except requests.exceptions.Timeout:
        print("\n❌ Request Timeout")
        print("Error: Server took too long to respond.")
        return 1
    except Exception as e:
        print("\n❌ Unexpected Error")
        print("Error:", str(e))
        return 1

if __name__ == "__main__":
    # Give server time to start if running together
    time.sleep(1)
    
    # Run test and exit with status code
    exit_code = run_test()
    exit(exit_code)