from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models, schemas, database
from database import engine, get_db

import time

# Create database tables with retries
# init_db()  # Commented out for in-memory mode

app = FastAPI(title="FastAPI + PostgreSQL CRUD")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI + PostgreSQL CRUD API"}

from services import user_service

@app.post("/users", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate):
    result = user_service.create_user(user)
    if "error" in result:
        raise HTTPException(status_code=result["status_code"], detail=result["error"])
    return result

# READ ALL
@app.get("/users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100):
    return user_service._users[skip : skip + limit]

# READ ONE
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int):
    for user in user_service._users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# UPDATE
@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_update: schemas.UserUpdate):
    for user in user_service._users:
        if user["id"] == user_id:
            if user_update.username:
                user["username"] = user_update.username
            if user_update.email:
                user["email"] = user_update.email
            if user_update.password:
                user["password"] = user_update.password
            return user
    raise HTTPException(status_code=404, detail="User not found")

# DELETE
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    for i, user in enumerate(user_service._users):
        if user["id"] == user_id:
            user_service._users.pop(i)
            return None
    raise HTTPException(status_code=404, detail="User not found")
