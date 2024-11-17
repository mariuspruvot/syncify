from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy.sql import func


class BaseModel(SQLModel):
    """Base model for all database models"""

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"server_default": func.now()},
    )
    updated_at: Optional[datetime] = Field(
        default=None, sa_column_kwargs={"onupdate": func.now()}
    )
