from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from typing import List
import schemas, models
from services import user_service
from database import SessionLocal, engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Registration API")

@app.get("/")
def read_root():
    return {"message": "FastAPI User Registration Service", "status": "running"}

@app.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user with username, password, and email.
    Returns 201 Created on success.
    """
    return user_service.create_user(db, user)

@app.get("/users", response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_by_id(db, user_id)

if __name__ == "__main__":
    import uvicorn
    # Using 8001 to avoid common conflicts
    uvicorn.run(app, host="127.0.0.1", port=8001)
