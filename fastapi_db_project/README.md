# FastAPI User Registration API

A simple, service-layer based User Registration API built with FastAPI and Python.

## Features
- **Create User**: Register a new user with username, password, and email.
- **List Users**: View all registered users.
- **In-Memory Storage**: Runs instantly without needing a database.
- **Swagger Docs**: Interactive API documentation.

## How to Run

### Option 1: One-Click Run (Permanent Command)
If you are on Windows, simply run this file in the project root:
```powershell
.\run.ps1
```

### Option 2: Manual Run
1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Run the server**:
   ```bash
   python main.py
   ```
   *The server will start on `http://127.0.0.1:8001`.*

## Testing the API

### 1. Interactive Docs
Visit `http://127.0.0.1:8001/docs` in your browser to test the endpoints directly.

### 2. Register a User (PowerShell)
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8001/users" -Method Post -ContentType "application/json" -Body '{"username": "Harish", "password": "welcome", "email": "hcmuleva@gmail.com"}'
```

### 3. View Users (Browser/GET)
Visit `http://127.0.0.1:8001/users` to see all registered users in JSON format.
