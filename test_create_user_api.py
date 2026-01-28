#!/usr/bin/env python3
"""
Test script for Create User API
This script tests the POST /users endpoint
"""
import subprocess
import time
import sys
import os

# Add current dir to path
sys.path.insert(0, '/workspaces/els')

# Start the server
print("Starting FastAPI server...")
server_process = subprocess.Popen(
    ["python", "/workspaces/els/main.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    cwd="/workspaces/els"
)

# Wait for server to start
time.sleep(3)

try:
    # Import requests after server starts
    import requests
    import json
    
    # Test data
    test_cases = [
        {
            "name": "Test 1: Valid user creation",
            "payload": {
                "username": "Harish",
                "password": "welcome",
                "email": "hcmuleva@gmail.com"
            },
            "expected_status": 201
        },
        {
            "name": "Test 2: Another valid user",
            "payload": {
                "username": "john_doe",
                "password": "password123",
                "email": "john@example.com"
            },
            "expected_status": 201
        },
        {
            "name": "Test 3: Duplicate username (should fail)",
            "payload": {
                "username": "Harish",
                "password": "different_pass",
                "email": "harish2@example.com"
            },
            "expected_status": 400
        },
        {
            "name": "Test 4: Invalid email format",
            "payload": {
                "username": "test_user",
                "password": "pass123",
                "email": "invalid_email"
            },
            "expected_status": 422
        }
    ]
    
    # Run tests
    url = "http://localhost:8000/users"
    print(f"\n{'='*60}")
    print("Testing Create User API")
    print(f"{'='*60}\n")
    
    for test in test_cases:
        print(f"➤ {test['name']}")
        try:
            response = requests.post(url, json=test['payload'], timeout=5)
            status_ok = response.status_code == test['expected_status']
            status_symbol = "✓" if status_ok else "✗"
            
            print(f"  {status_symbol} Status Code: {response.status_code} (expected {test['expected_status']})")
            print(f"  Response:")
            try:
                data = response.json()
                print(f"    {json.dumps(data, indent=4)}")
            except:
                print(f"    {response.text}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        print()
    
    # Test GET all users endpoint
    print(f"{'='*60}")
    print("Testing GET /users endpoint")
    print(f"{'='*60}\n")
    try:
        response = requests.get(url, timeout=5)
        print(f"✓ Status Code: {response.status_code}")
        print(f"Response:")
        data = response.json()
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"✗ Error: {e}")

finally:
    # Stop the server
    print("\nStopping server...")
    server_process.terminate()
    server_process.wait(timeout=5)
    print("Done!")
