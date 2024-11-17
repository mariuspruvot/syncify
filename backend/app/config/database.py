from sqlmodel import create_engine, Session
from backend.app.settings import GLOBAL_SETTINGS
import logging

sql_logger = logging.getLogger("sqlalchemy.engine")
sql_logger.setLevel(logging.WARNING)

DATABASE_URL = GLOBAL_SETTINGS.get_database_url()

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)


def get_db():
    """
    Provides a database session using a context manager.
    Session is automatically closed after use.

    Yields:
        Session: SQLModel session instance

    Raises:
        Exception: If there's an error during database operations
    """
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
