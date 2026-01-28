# Testing the Create User API with Postman

## Setup

1. **Start the FastAPI server:**
   ```bash
   cd /workspaces/els
   pip install -r requirements.txt
   python main.py
   ```

   The server will run on `http://localhost:8000`

2. **Access API Documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

---

## Create User Endpoint

### Request Details

- **HTTP Method:** POST
- **Endpoint:** `http://localhost:8000/users`
- **Content-Type:** application/json

### Request Body (JSON)

```json
{
  "username": "XYz",
  "password": "welcome",
  "email": "XYZa@gmail.com"
}
```

### Expected Response

**Status Code:** 201 (CREATED)

```json
{
  "id": 1,
  "username": "XYz",
  "email": "XYZa@gmail.com",
  "message": "User created successfully"
}
```

---

## Postman Testing Steps

### 1. Create a New Request

1. Open Postman
2. Click **New** → **HTTP Request**
3. Set the method to **POST**
4. Enter the URL: `http://localhost:8000/users`

### 2. Configure Headers

1. Go to the **Headers** tab
2. Add a header:
   - **Key:** `Content-Type`
   - **Value:** `application/json`

### 3. Add Request Body

1. Go to the **Body** tab
2. Select **raw**
3. Select **JSON** from the dropdown
4. Paste the request payload:

```json
{
  "username": "XYz",
  "password": "welcome",
  "email": "XYZa@gmail.com"
}
```

### 4. Send the Request

Click the **Send** button. You should receive a **201 CREATED** response with the user details.

---

## Test Cases

### Test Case 1: Valid User Creation

**Request:**
```json
{
  "username": "john_doe",
  "password": "secure123",
  "email": "john@example.com"
}
```

**Expected Response:** 201 Created

---

### Test Case 2: Duplicate Username

Create a user with the same username twice.

**Expected Response:** 400 Bad Request
```json
{
  "detail": "Username 'john_doe' already exists"
}
```

---

### Test Case 3: Invalid Email

**Request:**
```json
{
  "username": "test_user",
  "password": "password123",
  "email": "invalid-email"
}
```

**Expected Response:** 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "invalid email format"
    }
  ]
}
```

---

### Test Case 4: Short Password

**Request:**
```json
{
  "username": "test_user",
  "password": "short",
  "email": "test@example.com"
}
```

**Expected Response:** 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "password"],
      "msg": "String should have at least 6 characters"
    }
  ]
}
```

---

### Test Case 5: Get All Users

- **HTTP Method:** GET
- **Endpoint:** `http://localhost:8000/users`

**Expected Response:**
```json
[
  {
    "id": 1,
    "username": "XYz",
    "email": "XYZa@gmail.com"
  }
]
```

---

## API Documentation

The API automatically generates interactive documentation at:

- **Swagger UI (OpenAPI):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

You can use these interfaces to test the API directly without Postman.

---

## Troubleshooting

### Issue: Connection Refused
- Ensure the server is running: `python main.py`
- Check the port: The server runs on `localhost:8000`

### Issue: 422 Validation Error
- Check the JSON payload for correct field names
- Ensure email is in valid format
- Password must be at least 6 characters
- Username must be between 1-50 characters

### Issue: 400 Bad Request
- Username might already exist. Try a different username.
