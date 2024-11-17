import logging
from typing import Optional, Sequence

from sqlmodel import Session, select

from backend.app.models.tokens import Token
from backend.app.models.users import User
from backend.app.repositories.base_repository import AbstractRepository

logger = logging.getLogger(__name__)


class TokenRepository(AbstractRepository[Token, str]):
    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: str) -> Optional[Token]:
        """
        Retrieve a token for a specific user.

        Args:
            user_id: The ID of the user whose token to retrieve

        Returns:
            Optional[Token]: The token if found, None otherwise

        Raises:
            Exception: If there's an error during retrieval
        """
        try:
            statement = select(Token).where(Token.user_id == user_id)
            return self.db.exec(statement).first()
        except Exception as e:
            logger.error(f"Error retrieving token for user {user_id}: {str(e)}")
            raise

    def get_all_active_tokens(self) -> Sequence[Token]:
        """
        Retrieve all active tokens.

        Returns:
            Sequence[Token]: List of active tokens

        Raises:
            Exception: If there's an error during retrieval
        """
        try:
            statement = select(Token).where(Token.is_active == True)
            return self.db.exec(statement).all()
        except Exception as e:
            logger.error(f"Error retrieving active tokens: {str(e)}")
            raise

    def create(self, user: User) -> Token:
        """
        Create a new token for a user.

        Args:
            user: The user instance for whom to create the token

        Returns:
            Token: The newly created token instance

        Raises:
            Exception: If there's an error during token creation
        """
        try:
            logger.info(f"Creating token for user ID: {user.id}")
            new_token = Token(
                user_id=user.id, token=Token.generate_bearer_token(user.id)
            )

            self.db.add(new_token)
            self.db.commit()
            self.db.refresh(new_token)

            logger.info(f"Successfully created token for user ID: {user.id}")
            return new_token

        except Exception as e:
            logger.error(f"Error creating token for user {user.id}: {str(e)}")
            self.db.rollback()
            raise

    def delete(self, user_id: str) -> bool:
        """
        Delete a user's token.

        Args:
            user_id: The ID of the user whose token to delete

        Returns:
            bool: True if token was deleted, False if not found

        Raises:
            Exception: If there's an error during deletion
        """
        try:
            token = self.get(user_id)
            if token:
                self.db.delete(token)
                self.db.commit()
                logger.info(f"Successfully deleted token for user ID: {user_id}")
                return True
            logger.info(f"No token found to delete for user ID: {user_id}")
            return False
        except Exception as e:
            logger.error(f"Error deleting token for user {user_id}: {str(e)}")
            self.db.rollback()
            raise

    def list(self, limit: int = 10, start: int = 0) -> Sequence[Token]:
        """
        Retrieve a list of tokens with pagination.

        Args:
            limit: Maximum number of tokens to retrieve, defaults to 10
            start: Number of tokens to skip (offset), defaults to 0

        Returns:
            Sequence[Token]: List of tokens

        Raises:
            Exception: If there's an error during retrieval
        """
        try:
            statement = select(Token).offset(start).limit(limit)
            return self.db.exec(statement).all()
        except Exception as e:
            logger.error(f"Error listing tokens: {str(e)}")
            raise

    def update(self, user_id: str, update_data: dict) -> Optional[Token]:
        """
        Update a token's data.

        Args:
            user_id: The ID of the user whose token to update
            update_data: Dictionary containing the fields to update

        Returns:
            Optional[Token]: The updated token if found and updated, None otherwise

        Raises:
            Exception: If there's an error during update
        """
        try:
            statement = select(Token).where(Token.user_id == user_id)
            db_token = self.db.exec(statement).first()

            if not db_token:
                logger.info(f"No token found to update for user ID: {user_id}")
                return None

            for field, value in update_data.items():
                if value is not None and hasattr(db_token, field):
                    setattr(db_token, field, value)

            self.db.add(db_token)
            self.db.commit()
            self.db.refresh(db_token)

            logger.info(f"Successfully updated token for user ID: {user_id}")
            return db_token

        except Exception as e:
            logger.error(f"Error updating token for user {user_id}: {str(e)}")
            self.db.rollback()
            raise

    def deactivate(self, user_id: str) -> bool:
        """
        Deactivate a user's token.

        Args:
            user_id: The ID of the user whose token to deactivate

        Returns:
            bool: True if token was deactivated, False if not found

        Raises:
            Exception: If there's an error during deactivation
        """
        try:
            return self.update(user_id, {"is_active": False}) is not None
        except Exception as e:
            logger.error(f"Error deactivating token for user {user_id}: {str(e)}")
            raise

    def refresh_token(self, user_id: str) -> Optional[Token]:
        """
        Refresh a user's token.

        Args:
            user_id: The ID of the user whose token to refresh

        Returns:
            Optional[Token]: The refreshed token if found, None otherwise

        Raises:
            Exception: If there's an error during refresh
        """
        try:
            statement = select(Token).where(Token.user_id == user_id)
            db_token = self.db.exec(statement).first()

            if not db_token:
                logger.info(f"No token found to refresh for user ID: {user_id}")
                return None

            db_token.token = Token.generate_bearer_token(user_id)

            self.db.add(db_token)
            self.db.commit()
            self.db.refresh(db_token)

            logger.info(f"Successfully refreshed token for user ID: {user_id}")
            return db_token

        except Exception as e:
            logger.error(f"Error refreshing token for user {user_id}: {str(e)}")
            self.db.rollback()
            raise

    def get_by_token(self, token: str) -> Optional[Token]:
        """
        Retrieve a token by its token string.

        Args:
            token: The token string to search for

        Returns:
            Optional[Token]: The token if found, None otherwise

        Raises:
            Exception: If there's an error during retrieval
        """
        try:
            statement = select(Token).where(Token.token == token)
            return self.db.exec(statement).first()
        except Exception as e:
            logger.error(f"Error retrieving token: {str(e)}")
            raise
