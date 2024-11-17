import logging

logger = logging.getLogger("BACKEND")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
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
        "sqlalchemy.engine.transaction": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False,
        },
        "sqlalchemy.pool": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False,
        },
        "sqlalchemy.orm": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False,
        },
        "backend": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "uvicorn": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "fastapi": {"level": "INFO", "handlers": ["console"], "propagate": False},
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}
