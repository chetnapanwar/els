# Quick Start Guide

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Run the API

```bash
python main.py
```

**Output:**
```
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## 3. Test the API

### Option A: Interactive Documentation (Recommended)

Open your browser to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Try the endpoints directly from the UI!

### Option B: Using curl

Create a user:
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123","email":"test@example.com"}'
```

Get all users:
```bash
curl http://localhost:8000/users
```

### Option C: Using the test script

```bash
python test_api.py
```

### Option D: Using Postman

1. Open Postman
2. Create a POST request to `http://localhost:8000/users`
3. Set body to:
```json
{
  "username": "XYz",
  "password": "welcome",
  "email": "XYZa@gmail.com"
}
```
4. Send the request

**Expected response (Status 201):**
```json
{
  "id": 1,
  "username": "XYz",
  "email": "XYZa@gmail.com",
  "message": "User created successfully"
}
```

## 4. Project Structure

```
app/
├── models/           # Pydantic validation schemas
├── services/         # Business logic (service layer)
└── routes/           # API endpoints

main.py              # Application entry point
requirements.txt     # Dependencies
test_api.py          # Test script
```

## Common Test Cases

### Create a valid user
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "secure123",
    "email": "john@example.com"
  }'
```

### Try duplicate username (should fail)
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "different_password",
    "email": "different@example.com"
  }'
```

### Try invalid email (should fail)
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "password123",
    "email": "invalid-email"
  }'
```

### Try short password (should fail)
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "short",
    "email": "user@example.com"
  }'
```

## Validation Rules

- **Username**: 1-50 characters, must be unique
- **Password**: Minimum 6 characters
- **Email**: Valid email format

## HTTP Status Codes

- **201 Created**: User created successfully
- **400 Bad Request**: Duplicate username
- **422 Unprocessable Entity**: Invalid request data

## Need Help?

1. Check [API_README.md](API_README.md) for detailed documentation
2. Check [POSTMAN_TESTING.md](POSTMAN_TESTING.md) for Postman testing guide
3. Visit http://localhost:8000/docs for interactive API documentation
