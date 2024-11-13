class SpotifyBaseException(Exception):
    pass


class SpotifyAuthenticationException(SpotifyBaseException):
    pass


class SpotifyAPIException(SpotifyBaseException):
    pass
