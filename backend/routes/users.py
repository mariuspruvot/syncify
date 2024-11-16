from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from backend.factory.user_factory import UserFactory
from backend.repositories.user_repository import UserRepository
from backend.models.users import User
from backend.schemas.users import UserCreate, UserUpdate, UserList, UserResponse
from backend.config.database import SessionLocal, get_db
import logging

from backend.utils.validation.users import UserValidator

logger = logging.getLogger("USERS")

users_router = APIRouter()


@users_router.get("/health-check", tags=["users"])
def health_check():
    return {"status": "ok"}


@users_router.post(
    "/users", tags=["users"], status_code=201, response_model=UserResponse
)
def create_user(
    user: UserCreate, db: Annotated[SessionLocal, Depends(get_db)]
) -> UserResponse:
    """
    Creates a new user.
    """
    try:
        user_validator = UserValidator(UserRepository(db))
        user_validator.validate(user)

        user_repository = UserRepository(db)
        existing_user = user_repository.get_by_email(user.email)

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return UserFactory.from_db(user_repository.create(user))

    except HTTPException as he:
        raise he
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@users_router.get("/", tags=["users"], status_code=200, response_model=UserList)
def get_users(
    db: Annotated[SessionLocal, Depends(get_db)],
    limit: int = 10,
    offset: int = 0,
) -> UserList:
    """
    Gets a list of users with pagination.
    """
    try:
        user_repository = UserRepository(db)
        users = user_repository.list(limit, offset)
        total = db.query(User).count()
        users_response = [UserFactory.from_db(user) for user in users]
        return UserList(total=total, users=users_response)
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@users_router.get(
    "/{user_name}", tags=["users"], status_code=200, response_model=UserResponse
)
def get_user(
    user_name: str, db: Annotated[SessionLocal, Depends(get_db)]
) -> UserResponse:
    """
    Gets a specific user by ID.
    """
    try:
        user_repository = UserRepository(db)
        user = user_repository.get_by_display_name(user_name)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserFactory.from_db(user)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@users_router.patch(
    "/{user_id}", tags=["users"], status_code=200, response_model=UserResponse
)
def update_user(
    user_id: str, user: UserUpdate, db: Annotated[SessionLocal, Depends(get_db)]
) -> UserResponse:
    """
    Updates an existing user.
    """
    try:
        user_repository = UserRepository(db)
        if user.email:
            existing_user = user_repository.get_by_email(user.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(status_code=400, detail="Email already in use")

        updated_user = user_repository.update(user_id, user)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserFactory.from_db(updated_user)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@users_router.delete("/{user_id}", tags=["users"], status_code=204)
def delete_user(user_id: str, db: Annotated[SessionLocal, Depends(get_db)]):
    """
    Deletes an existing user.
    """
    try:
        user_repository = UserRepository(db)
        user = user_repository.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_repository.delete(user_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Routes pour les amis
@users_router.post("/{user_id}/friends/{friend_id}", tags=["users"], status_code=204)
def add_friend(
    user_id: str, friend_id: str, db: Annotated[SessionLocal, Depends(get_db)]
):
    """
    Adds a friend relationship between two users.
    """
    try:
        if user_id == friend_id:
            raise HTTPException(status_code=400, detail="Cannot add yourself as friend")

        user_repository = UserRepository(db)
        user = user_repository.get(user_id)
        friend = user_repository.get(friend_id)

        if not user or not friend:
            raise HTTPException(status_code=404, detail="User or friend not found")

        user_repository.add_friend(user_id, friend_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@users_router.delete("/{user_id}/friends/{friend_id}", tags=["users"], status_code=204)
def remove_friend(
    user_id: str, friend_id: str, db: Annotated[SessionLocal, Depends(get_db)]
):
    """
    Removes a friend relationship between two users.
    """
    try:
        user_repository = UserRepository(db)
        user = user_repository.get(user_id)
        friend = user_repository.get(friend_id)

        if not user or not friend:
            raise HTTPException(status_code=404, detail="User or friend not found")

        user_repository.remove_friend(user_id, friend_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
