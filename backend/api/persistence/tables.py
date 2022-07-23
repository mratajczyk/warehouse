from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    Text,
    BigInteger,
    UniqueConstraint,
    ForeignKey,
)

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
