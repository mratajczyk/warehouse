import uuid
from datetime import datetime

import pytest
from sqlalchemy import insert

from alembic.command import downgrade as alembic_downgrade
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from api.persistence.connection import SESSION_FACTORY
from api.persistence.tables import articles as articles_table
from api.persistence.tables import products as products_table
from api.persistence.tables import products_articles as products_articles_table
from api.persistence.tables import sales as sales_table
from api.persistence.tables import stock_updates as stock_updates_table
from api.schemas.internal import (Article, Product, ProductArticle, Sale,
                                  StockUpdate)

alembic_config = AlembicConfig("alembic.ini")


@pytest.fixture(autouse=False)
def database():
    """Fixture for setting up database for test
    @TODO - recreation is not optimal, implement creating database in first test, and truncating tables between tests
    """
    alembic_downgrade(alembic_config, "base")
    alembic_upgrade(alembic_config, "head")
    yield None


@pytest.fixture(autouse=False)
def session():
    """Fixture giving access to session"""
    session = SESSION_FACTORY()
    yield session
    session.close()


@pytest.fixture(autouse=False)
def dump_table(session):
    """Fixture giving access to callable that returns all contents of given table"""

    def _run(table):
        # Sort by all columns for deterministic output
        return session.query(table).order_by(*table.columns).all()

    yield _run


@pytest.fixture(autouse=False)
def set_example_database_products_articles(session):
    """Fixture that sets database in with Products/Articles/ProductsArticles for testing"""
    session.begin()
    session.execute(
        insert(products_table).values(
            [
                Product(product_id="1", name="Dining Chair"),
                Product(product_id="2", name="Dinning Table"),
            ]
        )
    )
    session.execute(
        insert(articles_table).values(
            [
                Article(article_id="1", name="leg"),
                Article(article_id="2", name="screw"),
                Article(article_id="3", name="seat"),
                Article(article_id="4", name="table_top"),
            ]
        )
    )
    session.execute(
        insert(products_articles_table).values(
            [
                ProductArticle(product_id="1", article_id="1", amount=4),
                ProductArticle(product_id="1", article_id="2", amount=8),
                ProductArticle(product_id="1", article_id="3", amount=1),
                ProductArticle(product_id="2", article_id="1", amount=4),
                ProductArticle(product_id="2", article_id="2", amount=8),
                ProductArticle(product_id="2", article_id="4", amount=1),
            ]
        )
    )
    session.commit()


@pytest.fixture(autouse=False)
def set_example_database_sale(session, set_example_database_products_articles):
    """Fixture that sets database in with Sale for testing"""
    sale = Sale(sale_id=uuid.uuid4(), product_id="1", amount=1)
    session.execute(insert(sales_table).values([sale]))
    session.execute(
        insert(stock_updates_table).values(
            [
                StockUpdate(
                    article_id="1",
                    value=10,
                    update_id=uuid.uuid4(),
                    sale_id=None,
                    created_at=datetime.now(),
                ),
                StockUpdate(
                    article_id="2",
                    value=5,
                    update_id=uuid.uuid4(),
                    sale_id=None,
                    created_at=datetime.now(),
                ),
                StockUpdate(
                    article_id="3",
                    value=3,
                    update_id=uuid.uuid4(),
                    sale_id=None,
                    created_at=datetime.now(),
                ),
                StockUpdate(
                    article_id="1",
                    value=-5,
                    update_id=uuid.uuid4(),
                    sale_id=sale["sale_id"],
                    created_at=datetime.now(),
                ),
                StockUpdate(
                    article_id="2",
                    value=-2,
                    update_id=uuid.uuid4(),
                    sale_id=sale["sale_id"],
                    created_at=datetime.now(),
                ),
                StockUpdate(
                    article_id="3",
                    value=-2,
                    update_id=uuid.uuid4(),
                    sale_id=sale["sale_id"],
                    created_at=datetime.now(),
                ),
            ]
        )
    )


@pytest.fixture(autouse=False)
def example_import_data():
    """Fixture providing data structured in import format"""
    return {
        "inventory": [
            {"art_id": "1", "name": "leg", "stock": "12"},
            {"art_id": "2", "name": "screw", "stock": "17"},
            {"art_id": "3", "name": "seat", "stock": "2"},
            {"art_id": "4", "name": "table top", "stock": "1"},
        ],
        "products": [
            {
                "name": "Dining Chair",
                "contain_articles": [
                    {"art_id": "1", "amount_of": "4"},
                    {"art_id": "2", "amount_of": "8"},
                    {"art_id": "3", "amount_of": "1"},
                ],
            },
            {
                "name": "Dinning Table",
                "contain_articles": [
                    {"art_id": "1", "amount_of": "4"},
                    {"art_id": "2", "amount_of": "8"},
                    {"art_id": "4", "amount_of": "1"},
                ],
            },
        ],
    }
