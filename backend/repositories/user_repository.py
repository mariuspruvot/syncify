from backend.models.users import User
from backend.repositories.base_repository import AbstractRepository
from backend.config.database import SessionLocal
from backend.schemas.users import UserCreate


class UserRepository(AbstractRepository[User, str]):
    def __init__(self, db: SessionLocal):
        self.db = db

    def create(self, instance: UserCreate) -> UserCreate:
        try:
            self.db.add(instance)
            self.db.commit()
            self.db.refresh(instance)
            return instance
        except Exception as e:
            self.db.rollback()
            raise e

    def get(self, id: str) -> User:
        try:
            return self.db.query(User).filter(User.id == id).first()
        except Exception as e:
            raise e

    def delete(self, id: str) -> None:
        try:
            user = self.get(id)
            if user:
                self.db.delete(user)
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def list(self, limit: int, start: int) -> list[User]:
        try:
            return self.db.query(User).limit(limit).offset(start).all()
        except Exception as e:
            raise e

    def update(self, id: str, instance: User) -> User:
        try:
            db_user = self.get(id)
            if db_user:
                for key, value in vars(instance).items():
                    if value is not None:
                        setattr(db_user, key, value)
                self.db.commit()
                self.db.refresh(db_user)
            return db_user
        except Exception as e:
            self.db.rollback()
            raise e

    def add_friend(self, user_id: str, friend_id: str) -> None:
        try:
            user = self.get(user_id)
            friend = self.get(friend_id)
            if user and friend:
                user.friends.append(friend)
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def remove_friend(self, user_id: str, friend_id: str) -> None:
        try:
            user = self.get(user_id)
            friend = self.get(friend_id)
            if user and friend:
                user.friends.remove(friend)
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_spotify_id(self, spotify_id: str) -> User:
        try:
            return self.db.query(User).filter(User.spotify_id == spotify_id).first()
        except Exception as e:
            raise e
