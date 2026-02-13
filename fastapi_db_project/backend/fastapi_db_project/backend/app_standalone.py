from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional

app = FastAPI(title="User Registration API")

# In-memory storage for quick testing
users_db = []
user_id_counter = 1

# Pydantic Models
class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

@app.get("/")
def read_root():
    return {"message": "FastAPI User Registration Service", "status": "running"}

@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    global user_id_counter
    
    # Check if email already exists
    for existing_user in users_db:
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
        if existing_user["username"] == user.username:
            raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create new user
    new_user = {
        "id": user_id_counter,
        "username": user.username,
        "email": user.email,
        "password": user.password  # In production, hash this!
    }
    
    users_db.append(new_user)
    user_id_counter += 1
    
    # Return response without password
    return UserResponse(
        id=new_user["id"],
        username=new_user["username"],
        email=new_user["email"]
    )

@app.get("/users/", response_model=List[UserResponse])
def get_all_users():
    return [
        UserResponse(id=u["id"], username=u["username"], email=u["email"])
        for u in users_db
    ]

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            return UserResponse(
                id=user["id"],
                username=user["username"],
                email=user["email"]
            )
    raise HTTPException(status_code=404, detail="User not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
