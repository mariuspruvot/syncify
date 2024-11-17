from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy import Text
from alembic import context
from backend.app.models import BaseModel

# Import all your models here
from backend.app.settings import GLOBAL_SETTINGS

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the database URL
DATABASE_URL = GLOBAL_SETTINGS.get_database_url()
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# add your model's MetaData object here
target_metadata = BaseModel.metadata


def render_item(type_, obj, autogen_context):
    """Apply custom rendering for selected items."""
    # Handle SQLModel string fields
    if type_ == "type":
        if hasattr(obj, "__class__") and obj.__class__.__name__ == "AutoString":
            return "sa.String"
        if isinstance(obj, Text):
            return "sa.Text()"
    return False


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_item=render_item,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_item=render_item,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
