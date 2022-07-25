import enum

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID

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

sales = Table(
    "sales",
    metadata,
    Column("sale_id", UUID(as_uuid=True), primary_key=True),
    Column("product_id", BigInteger, ForeignKey("products.product_id"), nullable=False),
    Column("amount", Integer, nullable=False),
)


stock_updates = Table(
    "stock_updates",
    metadata,
    Column("update_id", UUID(as_uuid=True), primary_key=True),
    Column("article_id", Integer, ForeignKey("articles.article_id"), nullable=False),
    Column("sale_id", UUID(as_uuid=True), ForeignKey("sales.sale_id"), nullable=True),
    Column("value", Integer, nullable=False),
    Column("created_at", DateTime, nullable=False),
)
