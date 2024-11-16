from backend.repositories.user_repository import UserRepository
from backend.schemas.users import UserCreate
from backend.utils.exceptions import EmailAlreadyExistsError, UserAlreadyExistsError, \
    PasswordNotStrongEnoughError


class UserValidator:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def validate(self, user: UserCreate) -> bool:
        self._validate_email(user.email)
        self._validate_display_name(user.display_name)
        self._validate_password(user.password)
        return True

    def _validate_email(self, email: str) -> bool:
        if self.user_repository.get_by_email(email):
            raise EmailAlreadyExistsError("Email already in use")
        return True

    def _validate_display_name(self, display_name: str) -> bool:
        if self.user_repository.get_by_display_name(display_name):
            raise UserAlreadyExistsError("Display name already in use")
        return True

    @staticmethod
    def _validate_password(password: str) -> bool:
        if not any(c.isupper() for c in password):
            raise PasswordNotStrongEnoughError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in password):
            raise PasswordNotStrongEnoughError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in password):
            raise PasswordNotStrongEnoughError("Password must contain at least one digit")
        return True
