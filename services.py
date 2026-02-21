from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import models, schemas

class UserService:
    def create_user(self, db: Session, user_data: schemas.UserCreate):
        # Check if user already exists
        db_user = db.query(models.User).filter(
            (models.User.email == user_data.email) | 
            (models.User.username == user_data.username)
        ).first()
        
        if db_user:
            if db_user.email == user_data.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Email already registered"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Username already taken"
            )

        # Create new user instance
        new_user = models.User(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password  # Note: Ideally hash this in a real app
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def get_all_users(self, db: Session):
        return db.query(models.User).all()

    def get_user_by_id(self, db: Session, user_id: int):
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found"
            )
        return user

# Global service instance
user_service = UserService()
