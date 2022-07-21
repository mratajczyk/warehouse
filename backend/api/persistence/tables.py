from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    Text,
    BigInteger,
    UniqueConstraint,
    create_engine,
    ForeignKey,
)
from sqlalchemy.orm import sessionmaker

from api.config.read import CONFIG

metadata = MetaData()

articles = Table(
    "articles",
    metadata,
    Column("article_id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
)


products = Table(
    "products",
    metadata,
    Column("product_id", BigInteger, primary_key=True),
    Column("name", Text, nullable=False),
)

products_articles = Table(
    "products_articles",
    metadata,
    Column("product_id", BigInteger, ForeignKey("products.product_id"), nullable=False),
    Column("article_id", Integer, ForeignKey("articles.article_id"), nullable=False),
    Column("amount", Integer, nullable=False),
    UniqueConstraint("product_id", "article_id", name="uix_1"),
)


def get_connection_url():
    return (
        f"postgresql+psycopg2://{CONFIG['DATABASE_USER']}:{CONFIG['DATABASE_PASSWORD']}@{CONFIG['DATABASE_HOST']}:"
        f"{CONFIG['DATABASE_PORT']}/{CONFIG['DATABASE_NAME']}"
    )


def get_engine():
    """Helper function for retrieving instance of database Engine"""
    return create_engine(get_connection_url())


SESSION_FACTORY = sessionmaker(bind=get_engine())
