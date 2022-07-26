import uuid
from datetime import datetime

import pytest
from sqlalchemy import insert

from api.persistence.tables import stock_updates as stock_updates_table
from api.schemas.internal import StockUpdate
from api.services.products import ProductStock, get_products_stock


@pytest.mark.parametrize(
    "article_stocks, expected",
    [
        (
            [
                ("1", 10),
                ("2", 10),
                ("3", 10),
                ("4", 10),
            ],
            [
                ProductStock(product_id="1", name="Dining Chair", stock=1.0),
                ProductStock(product_id="2", name="Dinning Table", stock=1.0),
            ],
        ),
        (
            [
                ("1", 11),
                ("2", 11),
                ("3", 11),
                ("4", 11),
            ],
            [
                ProductStock(product_id="1", name="Dining Chair", stock=1.0),
                ProductStock(product_id="2", name="Dinning Table", stock=1.0),
            ],
        ),
        (
            [
                ("1", 20),
                ("2", 20),
                ("3", 20),
                ("4", 20),
            ],
            [
                ProductStock(product_id="1", name="Dining Chair", stock=2),
                ProductStock(product_id="2", name="Dinning Table", stock=2),
            ],
        ),
        (
            [
                ("1", 4),
                ("2", 8),
                ("3", 0),
                ("4", 1),
            ],
            [
                ProductStock(product_id="1", name="Dining Chair", stock=0),
                ProductStock(product_id="2", name="Dinning Table", stock=1),
            ],
        ),
    ],
)
def test_get_products_stock(
    database, session, set_example_database_products_articles, article_stocks, expected
):
    session.begin()
    session.execute(
        insert(stock_updates_table).values(
            [
                StockUpdate(
                    article_id=article_id,
                    value=value,
                    update_id=uuid.uuid4(),
                    sale_id=None,
                    created_at=datetime.now(),
                )
                for article_id, value in article_stocks
            ]
        )
    )
    session.commit()
    assert set(get_products_stock()) == set(expected)
