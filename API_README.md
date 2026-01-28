# FastAPI User Creation API

A complete REST API implementation for user creation using FastAPI with a service-layer architecture.

## Project Structure

```
els/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py              # Pydantic request/response schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   └── user_routes.py       # API endpoints
│   └── services/
│       ├── __init__.py
│       └── user_service.py      # Business logic (service layer)
├── main.py                        # FastAPI application entry point
├── requirements.txt               # Python dependencies
├── test_api.py                    # Test script
└── POSTMAN_TESTING.md            # Postman testing guide
```

## Architecture

The application follows a **3-tier architecture**:

1. **Models Layer** (`app/models/user.py`):
   - Pydantic schemas for request validation
   - Response models for API responses

2. **Service Layer** (`app/services/user_service.py`):
   - Business logic for user operations
   - In-memory data storage
   - Data validation and processing

3. **Routes Layer** (`app/routes/user_routes.py`):
   - API endpoints
   - HTTP method handlers
   - Request/response management

## Features

✅ **POST /users** - Create a new user
- Validates request payload using Pydantic
- Returns 201 CREATED status code
- Prevents duplicate usernames
- Validates email format
- Enforces password minimum length

✅ **GET /users** - Retrieve all users
- Returns list of users (without passwords)

✅ **Request Validation**
- Username: 1-50 characters
- Password: Minimum 6 characters
- Email: Valid email format

✅ **Error Handling**
- 400 Bad Request: Duplicate username or validation errors
- 422 Unprocessable Entity: Invalid request payload
- Clear error messages

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup

1. **Clone the repository:**
```bash
cd /workspaces/els
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Running the API

### Start the FastAPI server:
```bash
python main.py
```

The server will start on: `http://localhost:8000`

### Interactive API Documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Create User

**Request:**
```
POST /users
Content-Type: application/json

{
  "username": "XYz",
  "password": "welcome",
  "email": "XYZa@gmail.com"
}
```

**Success Response (201 CREATED):**
```json
{
  "id": 1,
  "username": "XYz",
  "email": "XYZa@gmail.com",
  "message": "User created successfully"
}
```

**Error Response (400 BAD REQUEST):**
```json
{
  "detail": "Username 'XYz' already exists"
}
```

### Get All Users

**Request:**
```
GET /users
```

**Response:**
```json
[
  {
    "id": 1,
    "username": "XYz",
    "email": "XYZa@gmail.com"
  }
]
```

## Testing

### Using Python (Automated)

Run the included test script:
```bash
python test_api.py
```

This script tests:
- User creation
- Duplicate username prevention
- Invalid email validation
- Short password validation
- Get all users

### Using Postman (Manual)

See [POSTMAN_TESTING.md](POSTMAN_TESTING.md) for detailed Postman testing instructions.

### Using curl

```bash
# Create a user
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secure123","email":"john@example.com"}'

# Get all users
curl -X GET http://localhost:8000/users
```

## Service Layer Details

The `UserService` class handles all business logic:

```python
UserService.create_user(user_data: UserCreateRequest) -> UserCreateResponse
```

- Validates username uniqueness
- Stores user in in-memory database
- Returns user response with ID

### In-Memory Storage

Users are stored in a class-level dictionary:
```python
_users_db = {
    1: {"id": 1, "username": "XYz", "password": "welcome", "email": "XYZa@gmail.com"}
}
```

**Note**: This is reset when the application restarts. For production, replace with a real database.

## Request Validation

Pydantic handles automatic validation:

| Field | Validation |
|-------|-----------|
| username | Required, 1-50 characters |
| password | Required, minimum 6 characters |
| email | Required, valid email format |

## Response Codes

| Code | Description |
|------|-------------|
| 201 | User created successfully |
| 400 | Invalid request (duplicate username, etc.) |
| 422 | Validation error (invalid email, short password) |

## Dependencies

- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **pydantic** - Data validation
- **pydantic[email]** - Email validation

See [requirements.txt](requirements.txt) for versions.

## Production Considerations

For production deployment:

1. **Database**: Replace in-memory storage with PostgreSQL/MongoDB
2. **Password Security**: Hash passwords using bcrypt or argon2
3. **Authentication**: Implement JWT token-based auth
4. **Rate Limiting**: Add rate limiting to prevent abuse
5. **CORS**: Configure CORS for cross-origin requests
6. **Logging**: Add comprehensive logging
7. **Error Handling**: Implement detailed error handling
8. **Testing**: Add comprehensive unit and integration tests
9. **Environment Variables**: Use .env files for configuration
10. **API Versioning**: Implement API versioning

## Project Files

- [main.py](main.py) - FastAPI application entry point
- [app/models/user.py](app/models/user.py) - Pydantic models
- [app/services/user_service.py](app/services/user_service.py) - Service layer
- [app/routes/user_routes.py](app/routes/user_routes.py) - API routes
- [requirements.txt](requirements.txt) - Dependencies
- [test_api.py](test_api.py) - Test script
- [POSTMAN_TESTING.md](POSTMAN_TESTING.md) - Postman guide

## Example Usage

```python
from app.models.user import UserCreateRequest
from app.services.user_service import UserService

# Create a user
user_data = UserCreateRequest(
    username="john_doe",
    password="secure123",
    email="john@example.com"
)

response = UserService.create_user(user_data)
print(response)
# Output: UserCreateResponse(id=1, username='john_doe', email='john@example.com', message='User created successfully')
```

## License

MIT License

## Support

For issues or questions, refer to the FastAPI documentation: https://fastapi.tiangolo.com/
