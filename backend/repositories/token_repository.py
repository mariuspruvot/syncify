from backend.factory.user_factory import UserFactory
from backend.models.users import User
from backend.repositories.base_repository import AbstractRepository
from backend.config.database import SessionLocal
from backend.models.tokens import Token


class TokenRepository(AbstractRepository[User, str]):
    def __init__(self, db: SessionLocal):
        self.db = db

    def create(self, instance: User) -> Token:
        try:
            user_id = instance.id
            new_token = Token(
                user_id=user_id, token=Token.generate_bearer_token(user_id)
            )

            self.db.add(new_token)
            self.db.commit()

            self.db.refresh(new_token)

            self.db.refresh(instance)

            return new_token

        except Exception as e:
            self.db.rollback()
            raise e

    def get(self, user_id: str) -> Token:
        try:
            return self.db.query(Token).filter(Token.user_id == user_id).first()
        except Exception as e:
            raise e

    def delete(self, user_id: str) -> None:
        try:
            token = self.db.query(Token).filter(Token.user_id == user_id).first()
            if token:
                self.db.delete(token)
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def list(self, limit: int, start: int) -> list[Token]:
        try:
            tokens = self.db.query(Token).limit(limit).offset(start).all()
            if not tokens:
                return []
            return tokens
        except Exception as e:
            raise e

    def update(self, user_id: str, instance: User) -> Token:
        try:
            db_token = self.get(user_id)
            if db_token:
                for key, value in vars(instance).items():
                    if value is not None:
                        setattr(db_token, key, value)
                self.db.commit()
                self.db.refresh(db_token)
                return db_token
        except Exception as e:
            self.db.rollback()
            raise e
