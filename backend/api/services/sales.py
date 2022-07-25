import uuid
from datetime import datetime

from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError

from api.persistence.connection import SESSION_FACTORY
from api.persistence.tables import (
    products_articles as products_articles_table,
    stock_updates as stock_updates_table,
    sales as sales_table,
)
from api.schemas.internal import StockUpdate, Sale


class ProductNotFound(Exception):
    """Raised when requested Product is not found"""


def _generate_sale_id():
    """Helper function for creating sale_id"""
    return uuid.uuid4()


def register_sale(product_id: int, amount: int):
    """Process sale of Product"""

    if amount < 1:
        raise ValueError("Amount of sold Product must be greater than 0")

    sale_id = _generate_sale_id()
    columns = products_articles_table.columns
    statement = select([columns.article_id, columns.amount]).where(
        columns.product_id == product_id
    )
    with SESSION_FACTORY() as session:
        stock_updates = [
            StockUpdate(
                update_id=uuid.uuid4(),
                sale_id=sale_id,
                article_id=article_id,
                value=-abs(article_amount_in_product) * amount,
                created_at=datetime.now(),
            )
            for article_id, article_amount_in_product in session.execute(
                statement
            ).all()
        ]
        try:
            session.execute(
                insert(sales_table).values(
                    [Sale(sale_id=sale_id, product_id=product_id, amount=amount)]
                )
            )
        except IntegrityError as exception:
            if exception.orig.diag.constraint_name == "sales_product_id_fkey":
                raise ProductNotFound
        session.execute(insert(stock_updates_table).values(stock_updates))
        session.commit()


if __name__ == "__main__":
    register_sale(1, 2)
