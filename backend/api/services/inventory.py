from typing import List

from marshmallow import ValidationError
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.persistence.connection import SESSION_FACTORY
from api.persistence.tables import (
    products as products_table,
    articles as articles_table,
    products_articles as products_articles_table,
)
from api.schemas.external import ImportFile
from api.schemas.internal import Article, Product, ProductArticle
from api.services.perpare_import import transform_import_data


class UpdateInventoryException(Exception):
    """Raised when update inventory failed"""


# Prepare database insert statements for tables

statement_products = insert(products_table)
statement_articles = insert(articles_table)
statement_products_articles = insert(products_articles_table)

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
        except IntegrityError as e:
            raise UpdateInventoryException(e)


def deserialize_incoming_data(data: dict) -> dict:
    """Function that runs validation and deserialization of incoming data"""
    return ImportFile().load(data)


def run_update_inventory(data: bytes):
    """Function that encapsulates whole process of importing data

    :raises UpdateInventoryException: when non-recoverable problem with input data occurs
    """
    try:
        # Transform and validate contents of json file to dictionary with internal key names
        data = deserialize_incoming_data(data)
    except ValidationError as e:
        raise UpdateInventoryException(e)

    # Prepare internal representations of import data
    articles, products, products_articles, stock_updates = transform_import_data(data)
    # Persist data in database
    update_inventory(articles, products, products_articles)
