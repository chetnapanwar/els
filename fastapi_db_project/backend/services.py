from typing import List, Dict
import schemas

class UserService:
    def __init__(self):
        # In-memory storage for demonstration as per requirement
        self._users: List[Dict] = []
        self._id_counter = 1

    def create_user(self, user_data: schemas.UserCreate) -> Dict:
        # Check if email or username already exists in dummy storage
        for user in self._users:
            if user["email"] == user_data.email:
                return {"error": "Email already registered", "status_code": 400}
            if user["username"] == user_data.username:
                return {"error": "Username already taken", "status_code": 400}
        
        new_user = {
            "id": self._id_counter,
            "username": user_data.username,
            "email": user_data.email,
            "password": user_data.password  # In real app, hash this!
        }
        self._users.append(new_user)
        self._id_counter += 1
        return new_user

# Global service instance
user_service = UserService()
