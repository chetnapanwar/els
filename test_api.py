import requests
import json

def test_registration():
    url = "http://127.0.0.1:8001/users"
    payload = {
        "username": "Harish",
        "password": "welcome",
        "email": "hcmuleva@gmail.com"
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    print(f"Sending POST request to {url}...")
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("\nSUCCESS: User created successfully!")
        else:
            print("\nFAILED: Could not create user.")
            
    except requests.exceptions.ConnectionError:
        print("\nERROR: Could not connect to the server. Make sure main.py is running on port 8001.")

if __name__ == "__main__":
    test_registration()
