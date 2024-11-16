from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from backend.repositories.user_repository import UserRepository
from backend.models.users import User
from backend.schemas.users import UserCreate, UserUpdate, UserList, UserResponse
from backend.config.database import SessionLocal, get_db

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
        user_repository = UserRepository(db)
        existing_user = user_repository.get_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        created_user = user_repository.create(user)
        return UserResponse(**created_user.dict())
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@users_router.get("/users", tags=["users"], status_code=200, response_model=UserList)
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
        return UserList(total=total, users=users)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@users_router.get(
    "/users/{user_id}", tags=["users"], status_code=200, response_model=UserResponse
)
def get_user(
    user_id: str, db: Annotated[SessionLocal, Depends(get_db)]
) -> UserResponse:
    """
    Gets a specific user by ID.
    """
    try:
        user_repository = UserRepository(db)
        user = user_repository.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@users_router.patch(
    "/users/{user_id}", tags=["users"], status_code=200, response_model=UserResponse
)
def update_user(
    user_id: str, user: UserUpdate, db: Annotated[SessionLocal, Depends(get_db)]
) -> UserResponse:
    """
    Updates an existing user.
    """
    try:
        user_repository = UserRepository(db)
        # Vérifier si l'email est modifié et s'il existe déjà
        if user.email:
            existing_user = user_repository.get_by_email(user.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(status_code=400, detail="Email already in use")

        updated_user = user_repository.update(user_id, user)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@users_router.delete("/users/{user_id}", tags=["users"], status_code=204)
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
@users_router.post(
    "/users/{user_id}/friends/{friend_id}", tags=["users"], status_code=204
)
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


@users_router.delete(
    "/users/{user_id}/friends/{friend_id}", tags=["users"], status_code=204
)
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
