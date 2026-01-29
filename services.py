from typing import List, Dict
from fastapi import HTTPException
import schemas

class UserService:
    def __init__(self):
        self._users: List[Dict] = []
        self._id_counter = 1

    def create_user(self, user_data: schemas.UserCreate) -> Dict:
        # Check if email or username already exists
        for user in self._users:
            if user["email"] == user_data.email:
                raise HTTPException(status_code=400, detail="Email already registered")
            if user["username"] == user_data.username:
                raise HTTPException(status_code=400, detail="Username already taken")
        
        new_user = {
            "id": self._id_counter,
            "username": user_data.username,
            "email": user_data.email,
            "password": user_data.password
        }
        self._users.append(new_user)
        self._id_counter += 1
        return new_user

    def get_all_users(self) -> List[Dict]:
        return self._users

    def get_user_by_id(self, user_id: int) -> Dict:
        for user in self._users:
            if user["id"] == user_id:
                return user
        raise HTTPException(status_code=404, detail="User not found")

# Global service instance
user_service = UserService()
