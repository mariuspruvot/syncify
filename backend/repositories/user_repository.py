from backend.factory.user_factory import UserFactory
from backend.models.users import User
from backend.repositories.base_repository import AbstractRepository
from backend.config.database import SessionLocal
from backend.schemas.users import UserCreate


class UserRepository(AbstractRepository[User, str]):
    def __init__(self, db: SessionLocal):
        self.db = db

    def create(self, instance: UserCreate) -> User:
        try:
            user = UserFactory.from_create(instance)

            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise e

    def get(self, id: str) -> User | None:
        try:
            user = self.db.query(User).filter(User.id == id).first()
            if not user:
                return None
            return user
        except Exception as e:
            raise e

    def delete(self, id: str) -> None:
        try:
            user = self.db.query(User).filter(User.id == id).first()
            if user:
                self.db.delete(user)
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def list(self, limit: int, start: int) -> list[User]:
        try:
            users = self.db.query(User).limit(limit).offset(start).all()
            if not users:
                return []
            return users
        except Exception as e:
            raise e

    def update(self, id: str, instance: UserCreate) -> User:
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
            user = self.db.query(User).filter(User.id == user_id).first()
            friend = self.db.query(User).filter(User.id == friend_id).first()
            if user and friend:
                user.friends.append(friend)
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def remove_friend(self, user_id: str, friend_id: str) -> None:
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            friend = self.db.query(User).filter(User.id == friend_id).first()
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

    def get_by_email(self, email: str) -> User:
        try:
            return self.db.query(User).filter(User.email == email).first()
        except Exception as e:
            raise e

    def get_by_display_name(self, display_name: str) -> User:
        try:
            return self.db.query(User).filter(User.display_name == display_name).first()
        except Exception as e:
            raise e
