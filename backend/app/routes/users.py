from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from backend.app.repositories.user_repository import UserRepository
from backend.app.models.users import (
    User,
    UserOut,
    UserCreate,
    UserUpdate,
    PaginatedUsers,
)
from math import ceil
from backend.app.config.database import get_db
from backend.app.utils.validation.users import UserValidator
from backend.app.utils.exceptions import (
    EmailAlreadyExistsError,
    UserAlreadyExistsError,
    PasswordNotStrongEnoughError,
)
import logging

logger = logging.getLogger("USERS")

users_router = APIRouter()


@users_router.get("/health-check", tags=["users"])
def health_check() -> dict[str, str]:
    """Health check endpoint"""
    return {"status": "ok"}


@users_router.post("/", tags=["users"], status_code=201, response_model=UserOut)
def create_user(
    user_data: UserCreate, db: Annotated[Session, Depends(get_db)]
) -> UserOut:
    """
    Creates a new user.

    Args:
        user_data: User creation data
        db: Database session

    Returns:
        UserOut: Created user data

    Raises:
        HTTPException: If email exists or validation fails
    """
    try:
        user_repository = UserRepository(db)

        # Validate user data
        user_validator = UserValidator(user_repository)
        user_validator.validate(user_data)

        # Check if email exists
        if user_repository.get_by_email(user_data.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        # Create user and return sanitized data
        user = user_repository.create(user_data.model_dump())
        return UserOut.from_user(user)

    except (
        EmailAlreadyExistsError,
        UserAlreadyExistsError,
        PasswordNotStrongEnoughError,
    ) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@users_router.get("/", tags=["users"], response_model=PaginatedUsers)
def get_users(
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    per_page: int = 20,
) -> PaginatedUsers:
    """
    Gets a paginated list of users.

    Args:
        db: Database session
        page: Page number (starts at 1)
        per_page: Items per page

    Returns:
        PaginatedUsers: List of users with pagination info
    """
    try:
        user_repository = UserRepository(db)
        total = db.exec(select(func.count(User.id))).first()
        users = user_repository.list(per_page, (page - 1) * per_page)

        return PaginatedUsers(
            total=total,
            users=[
                UserOut.from_user(user, include_friends_count=True) for user in users
            ],
            page=page,
            per_page=per_page,
            pages=ceil(total / per_page),
        )
    except Exception as e:
        logger.error(f"Error getting users: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@users_router.get("/{username}", tags=["users"], response_model=UserOut)
def get_user(username: str, db: Annotated[Session, Depends(get_db)]) -> UserOut:
    """
    Gets a specific user by username.

    Args:
        username: User's display name
        db: Database session

    Returns:
        UserOut: User data

    Raises:
        HTTPException: If user not found
    """
    try:
        user_repository = UserRepository(db)
        user = user_repository.get_by_display_name(username)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return UserOut.from_user(user, include_friends_count=True)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error getting user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@users_router.patch("/{user_id}", tags=["users"], response_model=UserOut)
def update_user(
    user_id: str, user_data: UserUpdate, db: Annotated[Session, Depends(get_db)]
) -> UserOut:
    """
    Updates an existing user.

    Args:
        user_id: User's ID
        user_data: Update data
        db: Database session

    Returns:
        UserOut: Updated user data

    Raises:
        HTTPException: If user not found or email exists
    """
    try:
        user_repository = UserRepository(db)

        # Check email uniqueness if provided
        if user_data.email:
            existing_user = user_repository.get_by_email(user_data.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(status_code=400, detail="Email already in use")

        updated_user = user_repository.update(
            user_id, user_data.model_dump(exclude_unset=True)
        )
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")

        return UserOut.from_user(updated_user)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@users_router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str, db: Annotated[Session, Depends(get_db)]) -> None:
    """
    Deletes an existing user.

    Args:
        user_id: User's ID
        db: Database session

    Raises:
        HTTPException: If user not found
    """
    try:
        user_repository = UserRepository(db)
        if not user_repository.delete(user_id):
            raise HTTPException(status_code=404, detail="User not found")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@users_router.post("/{user_id}/friends/{friend_id}", status_code=204)
def add_friend(
    user_id: str, friend_id: str, db: Annotated[Session, Depends(get_db)]
) -> None:
    """
    Adds a friend relationship between users.

    Args:
        user_id: User's ID
        friend_id: Friend's ID
        db: Database session

    Raises:
        HTTPException: If users not found or invalid request
    """
    try:
        if user_id == friend_id:
            raise HTTPException(status_code=400, detail="Cannot add yourself as friend")

        user_repository = UserRepository(db)
        if not user_repository.add_friend(user_id, friend_id):
            raise HTTPException(status_code=404, detail="User or friend not found")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error adding friend: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@users_router.delete("/{user_id}/friends/{friend_id}", status_code=204)
def remove_friend(
    user_id: str, friend_id: str, db: Annotated[Session, Depends(get_db)]
) -> None:
    """
    Removes a friend relationship between users.

    Args:
        user_id: User's ID
        friend_id: Friend's ID
        db: Database session

    Raises:
        HTTPException: If users not found
    """
    try:
        user_repository = UserRepository(db)
        if not user_repository.remove_friend(user_id, friend_id):
            raise HTTPException(status_code=404, detail="User or friend not found")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error removing friend: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
