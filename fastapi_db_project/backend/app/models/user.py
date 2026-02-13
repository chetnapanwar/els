from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    """Request schema for creating a new user"""
    username: str = Field(..., min_length=1, max_length=50, description="Username for the account")
    password: str = Field(..., min_length=6, max_length=100, description="Password (minimum 6 characters)")
    email: EmailStr = Field(..., description="Valid email address")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "XYz",
                "password": "welcome",
                "email": "XYZa@gmail.com"
            }
        }


class UserCreateResponse(BaseModel):
    """Response schema for user creation"""
    id: int
    username: str
    email: str
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "XYz",
                "email": "XYZa@gmail.com",
                "message": "User created successfully"
            }
        }
