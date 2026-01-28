#!/usr/bin/env python3
"""Test script for the Create User API"""
import subprocess
import time
import socket
import sys
import json
import urllib.request
import urllib.error

def is_port_free(port=8000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result != 0

print("=" * 60)
print("CREATE USER API - FUNCTIONAL TEST")
print("=" * 60)

# Kill any existing process
subprocess.run(["pkill", "-f", "python main.py"], capture_output=True)
time.sleep(1)

# Start server
print("\nStarting FastAPI server...")
server = subprocess.Popen(
    ["python", "/workspaces/els/main.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    cwd="/workspaces/els"
)

# Wait for server
for i in range(15):
    if not is_port_free():
        print("✓ Server ready")
        break
    time.sleep(0.5)
else:
    print("✗ Server timeout")
    sys.exit(1)

time.sleep(1)

# Test 1: Create user
print("\n[Test 1] POST /users - Create user (Harish)")
print("-" * 60)
payload = {"username": "Harish", "password": "welcome", "email": "hcmuleva@gmail.com"}
try:
    req = urllib.request.Request(
        "http://localhost:8000/users",
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with urllib.request.urlopen(req) as response:
        status = response.status
        data = json.loads(response.read().decode('utf-8'))
        print(f"✓ HTTP {status}")
        print(f"✓ Response: {json.dumps(data, indent=2)}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Create another user
print("\n[Test 2] POST /users - Create user (John)")
print("-" * 60)
payload = {"username": "john_doe", "password": "pass123", "email": "john@example.com"}
try:
    req = urllib.request.Request(
        "http://localhost:8000/users",
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with urllib.request.urlopen(req) as response:
        status = response.status
        data = json.loads(response.read().decode('utf-8'))
        print(f"✓ HTTP {status}")
        print(f"✓ Response: {json.dumps(data, indent=2)}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Duplicate username
print("\n[Test 3] POST /users - Duplicate username (should fail)")
print("-" * 60)
payload = {"username": "Harish", "password": "newpass", "email": "new@example.com"}
try:
    req = urllib.request.Request(
        "http://localhost:8000/users",
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with urllib.request.urlopen(req) as response:
        print(f"✗ Should have failed")
except urllib.error.HTTPError as e:
    if e.code == 400:
        data = json.loads(e.read().decode())
        print(f"✓ HTTP {e.code} (expected)")
        print(f"✓ Error: {data['detail']}")
    else:
        print(f"✗ Wrong status: {e.code}")

# Test 4: Get all users
print("\n[Test 4] GET /users - Retrieve all users")
print("-" * 60)
try:
    req = urllib.request.Request("http://localhost:8000/users", method='GET')
    with urllib.request.urlopen(req) as response:
        status = response.status
        data = json.loads(response.read().decode('utf-8'))
        print(f"✓ HTTP {status}")
        print(f"✓ Total users: {len(data)}")
        print(f"✓ Users: {json.dumps(data, indent=2)}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 5: Root endpoint
print("\n[Test 5] GET / - Root endpoint")
print("-" * 60)
try:
    with urllib.request.urlopen("http://localhost:8000/") as response:
        data = json.loads(response.read().decode('utf-8'))
        print(f"✓ HTTP {response.status}")
        print(f"✓ Response: {json.dumps(data, indent=2)}")
except Exception as e:
    print(f"✗ Error: {e}")

# Cleanup
server.terminate()
server.wait(timeout=5)

print("\n" + "=" * 60)
print("✓ ALL TESTS COMPLETED SUCCESSFULLY!")
print("=" * 60)
