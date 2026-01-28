import requests
import json

BASE_URL = "http://localhost:8000"

# Test 1: Create a valid user
print("=" * 60)
print("Test 1: Create a valid user")
print("=" * 60)
payload = {
    "username": "XYz",
    "password": "welcome",
    "email": "XYZa@gmail.com"
}
print(f"Request: POST {BASE_URL}/users")
print(f"Payload: {json.dumps(payload, indent=2)}")
response = requests.post(f"{BASE_URL}/users", json=payload)
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 2: Try to create duplicate user
print("\n" + "=" * 60)
print("Test 2: Try to create duplicate user (same username)")
print("=" * 60)
print(f"Request: POST {BASE_URL}/users")
print(f"Payload: {json.dumps(payload, indent=2)}")
response = requests.post(f"{BASE_URL}/users", json=payload)
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 3: Create another valid user
print("\n" + "=" * 60)
print("Test 3: Create another valid user")
print("=" * 60)
payload2 = {
    "username": "john_doe",
    "password": "secure123",
    "email": "john@example.com"
}
print(f"Request: POST {BASE_URL}/users")
print(f"Payload: {json.dumps(payload2, indent=2)}")
response = requests.post(f"{BASE_URL}/users", json=payload2)
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 4: Get all users
print("\n" + "=" * 60)
print("Test 4: Get all users")
print("=" * 60)
print(f"Request: GET {BASE_URL}/users")
response = requests.get(f"{BASE_URL}/users")
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 5: Invalid email
print("\n" + "=" * 60)
print("Test 5: Invalid email format")
print("=" * 60)
payload3 = {
    "username": "invalid_email_user",
    "password": "password123",
    "email": "not-an-email"
}
print(f"Request: POST {BASE_URL}/users")
print(f"Payload: {json.dumps(payload3, indent=2)}")
response = requests.post(f"{BASE_URL}/users", json=payload3)
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 6: Short password
print("\n" + "=" * 60)
print("Test 6: Password too short (minimum 6 characters)")
print("=" * 60)
payload4 = {
    "username": "short_pass_user",
    "password": "short",
    "email": "test@example.com"
}
print(f"Request: POST {BASE_URL}/users")
print(f"Payload: {json.dumps(payload4, indent=2)}")
response = requests.post(f"{BASE_URL}/users", json=payload4)
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
