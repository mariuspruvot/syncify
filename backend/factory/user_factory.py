from backend.models.users import User
from backend.schemas.users import UserCreate, UserInApp


class UserFactory:
    """
    Factory class working as a bridge between the database and pydantic models.
    """

    @staticmethod
    def from_db(user: User) -> UserInApp:
        """
        Converts a User model instance into a UserCreate schema instance.
        """
        return UserInApp(
            id=user.id,
            display_name=user.display_name,
            country=user.country,
            email=user.email,
            avatar=user.avatar,
            spotify_id=user.spotify_id,
            is_online=user.is_online,
            currently_playing=user.currently_playing,
        )

    @staticmethod
    def from_create(user: UserCreate) -> User:
        """
        Converts a UserCreate schema instance into a User model instance.
        """
        user_model = User(
            spotify_id=user.spotify_id,
            display_name=user.display_name,
            country=user.country,
            email=user.email,
            avatar=user.avatar,
            is_online=user.is_online,
            currently_playing=user.currently_playing,
            password_hash=user.password_hash,
        )
        user_model.set_password(user.password_hash)
        return user_model
