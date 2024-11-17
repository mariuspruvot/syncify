from typing import Optional, List, Sequence

from sqlmodel import Session, select
from backend.app.models.users import User
from backend.app.repositories.base_repository import AbstractRepository
import logging

logger = logging.getLogger(__name__)


class UserRepository(AbstractRepository[User, str]):
    def __init__(self, db: Session):
        self.db = db

    def get(self, id: str) -> Optional[User]:
        statement = select(User).where(User.id == id)
        return self.db.exec(statement).first()

    def get_by_spotify_id(self, spotify_id: str) -> Optional[User]:
        statement = select(User).where(User.spotify_id == spotify_id)
        return self.db.exec(statement).first()

    def get_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return self.db.exec(statement).first()

    def get_by_display_name(self, display_name: str) -> Optional[User]:
        statement = select(User).where(User.display_name == display_name)
        return self.db.exec(statement).first()

    def list(self, limit: int, start: int) -> Sequence[User]:
        statement = select(User).limit(limit).offset(start)
        return self.db.exec(statement).all()

    def create(self, user_data: dict) -> User:
        """
        Creates a new user with validated data.

        Args:
            user_data: Dictionary containing user data

        Returns:
            User: The created user instance

        Raises:
            Exception: If there's an error during user creation
        """
        try:
            logger.info(f"Creating user with data: {user_data}")
            user = User(**user_data)

            if "password" in user_data:
                user.set_password(user_data["password"])

            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

            logger.info(f"Successfully created user with ID: {user.id}")
            return user
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            self.db.rollback()
            raise

    def update(self, id: str, update_data: dict) -> Optional[User]:
        """
        Updates a user with the provided data.

        Args:
            id: The user's ID
            update_data: Dictionary containing fields to update

        Returns:
            Optional[User]: The updated user or None if not found

        Raises:
            Exception: If there's an error during update
        """
        try:
            db_user = self.get(id)
            if not db_user:
                return None

            for field, value in update_data.items():
                if value is not None and hasattr(db_user, field):
                    if field == "password":
                        db_user.set_password(value)
                    else:
                        setattr(db_user, field, value)

            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except Exception as e:
            self.db.rollback()
            raise

    def delete(self, id: str) -> bool:
        """
        Deletes a user by ID.

        Args:
            id: The user's ID

        Returns:
            bool: True if user was deleted, False if not found

        Raises:
            Exception: If there's an error during deletion
        """
        try:
            user = self.get(id)
            if user:
                self.db.delete(user)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            raise

    def add_friend(self, user_id: str, friend_id: str) -> bool:
        """
        Adds a friendship relationship between two users.

        Args:
            user_id: ID of the user initiating the friendship
            friend_id: ID of the user to be added as friend

        Returns:
            bool: True if friendship was created, False if users not found or already friends

        Raises:
            Exception: If there's an error during the operation
        """
        try:
            statement_user = select(User).where(User.id == user_id)
            statement_friend = select(User).where(User.id == friend_id)

            user = self.db.exec(statement_user).first()
            friend = self.db.exec(statement_friend).first()

            if not user or not friend:
                return False

            if friend not in user.friends:
                user.friends.append(friend)
                self.db.commit()
                return True

            return False
        except Exception as e:
            self.db.rollback()
            raise

    def remove_friend(self, user_id: str, friend_id: str) -> bool:
        """
        Removes a friendship relationship between two users.

        Args:
            user_id: ID of the user removing the friendship
            friend_id: ID of the user to be removed from friends

        Returns:
            bool: True if friendship was removed, False if users not found or weren't friends

        Raises:
            Exception: If there's an error during the operation
        """
        try:
            statement_user = select(User).where(User.id == user_id)
            statement_friend = select(User).where(User.id == friend_id)

            user = self.db.exec(statement_user).first()
            friend = self.db.exec(statement_friend).first()

            if not user or not friend:
                return False

            if friend in user.friends:
                user.friends.remove(friend)
                self.db.commit()
                return True

            return False
        except Exception as e:
            self.db.rollback()
            raise

    def get_friends(self, user_id: str) -> List[User]:
        """
        Retrieves the list of friends for a user.

        Args:
            user_id: The user's ID

        Returns:
            List[User]: List of user's friends, empty list if user not found
        """
        statement = select(User).where(User.id == user_id)
        user = self.db.exec(statement).first()
        return user.friends if user else []
