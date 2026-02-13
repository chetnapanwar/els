from fastapi import FastAPI, status
from typing import List
import schemas
from services import user_service

app = FastAPI(title="User Registration API")

@app.get("/")
def read_root():
    return {"message": "FastAPI User Registration Service", "status": "running"}

@app.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate):
    return user_service.create_user(user)

@app.get("/users", response_model=List[schemas.UserResponse])
def get_all_users():
    return user_service.get_all_users()

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int):
    return user_service.get_user_by_id(user_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
