from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.config.read import CONFIG


def get_connection_url():
    return (
        f"postgresql+psycopg2://{CONFIG['DATABASE_USER']}:{CONFIG['DATABASE_PASSWORD']}@{CONFIG['DATABASE_HOST']}:"
        f"{CONFIG['DATABASE_PORT']}/{CONFIG['DATABASE_NAME']}"
    )


def get_engine():
    """Helper function for retrieving instance of database Engine"""
    return create_engine(get_connection_url())


SESSION_FACTORY = sessionmaker(bind=get_engine())
