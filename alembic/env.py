from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
import os 
from dotenv import load_dotenv
import sys 
from alembic import context

# start >> Custom Configuration
production_env = os.getenv("DEBUG", "True").lower() == "false"

if production_env:
    env_file = ".env.prod"
else:
    env_file = ".env.dev"
load_dotenv(dotenv_path =env_file)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

print(BASE_DIR, "BASE_DIR")
# << End Custom Configuration

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# start >> Custom Configuration

DATABASE_URL_VALUE = os.getenv("DATABASE_URL_VALUE")

config.set_main_option("sqlalchemy.url", DATABASE_URL_VALUE)

# << End Custom Configuration


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

#  start >> Custom Configuration

from database import Base
target_metadata = Base.metadata

# << End Custom Configuration

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
