from typing import List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.persistence.tables import (
    products as products_table,
    articles as articles_table,
    SESSION_FACTORY,
    products_articles,
)
from api.schemas.internal import Article, Product, ProductArticle


class UpdateInventoryException(Exception):
    """Raised when update inventory failed"""


# Prepare database insert statements for tables

statement_products = insert(products_table)
statement_articles = insert(articles_table)
statement_products_articles = insert(products_articles)

# Make statements to work as upsert
statement_articles = statement_articles.on_conflict_do_nothing(
    constraint="articles_pkey"
)
statement_products = statement_products.on_conflict_do_nothing(
    constraint="products_pkey"
)
# We assume that Product definition could not change
statement_products_articles = statement_products_articles.on_conflict_do_nothing(
    constraint="uix_1"
)


def update_inventory(
    articles_data: List[Article],
    products_data: List[Product],
    product_articles_data: List[ProductArticle],
):
    with SESSION_FACTORY() as session:
        session: Session
        try:
            if articles_data:
                session.execute(statement_articles.values(articles_data))
            if products_data:
                session.execute(statement_products.values(products_data))
            if product_articles_data:
                session.execute(
                    statement_products_articles.values(product_articles_data)
                )
            session.commit()
        except IntegrityError:
            raise UpdateInventoryException
