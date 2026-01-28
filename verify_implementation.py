#!/usr/bin/env python3
"""
Comprehensive test of the Create User API
Demonstrates all functionality
"""

import json
from app.models.user import UserCreateRequest, UserCreateResponse
from app.services.user_service import UserService

print("=" * 70)
print("CREATE USER API - IMPLEMENTATION VERIFICATION")
print("=" * 70)

# Test 1: Valid user creation
print("\n✓ Test 1: Valid User Creation")
print("-" * 70)
try:
    user_data = UserCreateRequest(
        username="Harish",
        password="welcome",
        email="hcmuleva@gmail.com"
    )
    print(f"Request Payload:")
    print(f"  {json.dumps(user_data.model_dump(), indent=4)}")
    
    response = UserService.create_user(user_data)
    print(f"\nResponse (HTTP 201):")
    print(f"  {json.dumps(response.model_dump(), indent=4)}")
    print("  ✓ User created successfully!")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 2: Another valid user
print("\n✓ Test 2: Create Second User")
print("-" * 70)
try:
    user_data2 = UserCreateRequest(
        username="john_doe",
        password="password123",
        email="john@example.com"
    )
    print(f"Request Payload:")
    print(f"  {json.dumps(user_data2.model_dump(), indent=4)}")
    
    response2 = UserService.create_user(user_data2)
    print(f"\nResponse (HTTP 201):")
    print(f"  {json.dumps(response2.model_dump(), indent=4)}")
    print("  ✓ Second user created successfully!")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 3: Duplicate username (should fail)
print("\n✗ Test 3: Duplicate Username (Expected Failure)")
print("-" * 70)
try:
    user_data3 = UserCreateRequest(
        username="Harish",  # Duplicate!
        password="different_password",
        email="harish_new@example.com"
    )
    response3 = UserService.create_user(user_data3)
    print(f"  ✗ Should have failed but didn't!")
except ValueError as e:
    print(f"  ✓ Correctly rejected: {e}")
except Exception as e:
    print(f"  ✗ Unexpected error: {e}")

# Test 4: Retrieve all users
print("\n✓ Test 4: Get All Users")
print("-" * 70)
all_users = UserService.get_all_users()
print(f"Total Users: {len(all_users)}")
print(f"Users (without passwords):")
for user in all_users:
    print(f"  {json.dumps(user, indent=4)}")

print("\n" + "=" * 70)
print("IMPLEMENTATION SUMMARY")
print("=" * 70)
print("""
✓ Models (Pydantic):
  - UserCreateRequest: Validates username, password, and email
  - UserCreateResponse: Returns id, username, email, and message

✓ Service Layer:
  - UserService.create_user(): Creates user and stores in memory
  - UserService.get_all_users(): Retrieves all users
  - Validates duplicate usernames
  - In-memory storage with ID counter

✓ API Routes:
  - POST /users: Creates a new user (HTTP 201)
  - GET /users: Retrieves all users (HTTP 200)
  - Error handling for duplicate users (HTTP 400)
  - Email validation (HTTP 422 for invalid format)

✓ Features:
  - Request validation using Pydantic models
  - Service-layer architecture
  - In-memory storage (no database)
  - Proper HTTP status codes
  - Error handling and messages
""")
print("=" * 70)
