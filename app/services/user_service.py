from app.models.user import UserCreateRequest, UserCreateResponse


class UserService:
    """Service layer for user operations"""
    
    # In-memory storage for users
    _users_db = {}
    _user_id_counter = 1
    
    @classmethod
    def create_user(cls, user_data: UserCreateRequest) -> UserCreateResponse:
        """
        Create a new user and store in memory
        
        Args:
            user_data: UserCreateRequest containing username, password, and email
            
        Returns:
            UserCreateResponse with created user details
            
        Raises:
            ValueError: If username already exists
        """
        # Check if username already exists
        for user in cls._users_db.values():
            if user["username"] == user_data.username:
                raise ValueError(f"Username '{user_data.username}' already exists")
        
        # Create new user
        user_id = cls._user_id_counter
        cls._users_db[user_id] = {
            "id": user_id,
            "username": user_data.username,
            "password": user_data.password,  # In production, hash the password
            "email": user_data.email
        }
        cls._user_id_counter += 1
        
        # Return response
        return UserCreateResponse(
            id=user_id,
            username=user_data.username,
            email=user_data.email,
            message="User created successfully"
        )
    
    @classmethod
    def get_all_users(cls) -> list:
        """Get all users (without passwords)"""
        users = []
        for user in cls._users_db.values():
            users.append({
                "id": user["id"],
                "username": user["username"],
                "email": user["email"]
            })
        return users
