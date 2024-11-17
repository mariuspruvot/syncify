class UserAlreadyExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class PasswordNotStrongEnoughError(Exception):
    pass
