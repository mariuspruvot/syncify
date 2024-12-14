import logging
from logging.config import dictConfig
import colorlog

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(asctime)s%(reset)s %(cyan)s[%(name)s]%(reset)s %(message)s",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green,bold",
                "WARNING": "yellow,bold",
                "ERROR": "red,bold",
                "CRITICAL": "red,bg_white,bold",
            },
            "secondary_log_colors": {},
            "style": "%",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "colored",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "sqlalchemy": {"level": "WARNING", "handlers": ["console"], "propagate": False},
        "sqlalchemy.engine": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False,
        },
        "uvicorn": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "uvicorn.access": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "uvicorn.asgi": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "backend": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "fastapi": {"level": "INFO", "handlers": ["console"], "propagate": False},
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

LOGGER = logging.getLogger("BACKEND")
dictConfig(LOGGING_CONFIG)
