from fastapi import APIRouter, HTTPException, status
from app.models.user import UserCreateRequest, UserCreateResponse
from app.services.user_service import UserService


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateRequest) -> UserCreateResponse:
    """
    Create a new user
    
    Request body:
    - **username**: Username for the account (1-50 characters)
    - **password**: Password (minimum 6 characters)
    - **email**: Valid email address
    
    Returns:
    - **id**: User ID
    - **username**: Created username
    - **email**: Created email
    - **message**: Success message
    """
    try:
        user = UserService.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("", response_model=list)
async def get_all_users() -> list:
    """
    Retrieve all users (returns list of users without passwords)
    """
    return UserService.get_all_users()
