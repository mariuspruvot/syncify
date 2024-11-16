from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from backend.factory.user_factory import UserFactory
from backend.repositories.token_repository import TokenRepository
from backend.repositories.user_repository import UserRepository
from backend.schemas.auth import Login
from backend.schemas.users import UserInApp, UserCreate
from backend.utils.exceptions import UserNotFoundError
from backend.config.database import SessionLocal, get_db

app_auth_router = APIRouter()


@app_auth_router.post("/login", tags=["app_auth"], status_code=200)
def login(
    user_login: Login, db: Annotated[SessionLocal, Depends(get_db)]
) -> dict[str, str]:
    """
    Logs in a user and returns a JWT token.
    """
    try:
        user_repository = UserRepository(db)
        user_in_db = user_repository.get_by_email(user_login.email)

        if not user_in_db:
            raise UserNotFoundError("User not found")

        if not user_in_db.check_password(user_login.password):
            raise HTTPException(status_code=400, detail="Incorrect password")

        token = TokenRepository(db).create(user_in_db)

        return {"token": token.token}

    except HTTPException as he:
        raise he
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app_auth_router.post("/logout", tags=["app_auth"], status_code=204)
def logout(token: str, db: Annotated[SessionLocal, Depends(get_db)]) -> None:
    """
    Logs out a user and invalidates the JWT token.
    """
    try:
        token_repository = TokenRepository(db)
        token_repository.delete(token)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app_auth_router.post("/register", tags=["app_auth"], status_code=201)
def register(user: UserCreate, db: Annotated[SessionLocal, Depends(get_db)]):
    """
    Registers a new user.
    """
    try:
        user_repository = UserRepository(db)
        existing_user = user_repository.get_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        created_user = user_repository.create(user)
        return UserFactory.from_db(created_user)
    except HTTPException as he:
        raise he
