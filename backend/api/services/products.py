from collections import namedtuple
from typing import List

from api.persistence.connection import SESSION_FACTORY

ProductStock = namedtuple("ProductStock", ["product_id", "name", "stock"])


def get_products_stock() -> List[ProductStock]:
    """Function returning available stock for Products

    @TODO - right now it's an big SQL statement, will try to convert it to SQLAlchemy code if there is time
    """
    statement = """
    SELECT
        products_articles.product_id,
        products.name,
        MIN(FLOOR(coalesce(in_stock.in_stock, 0) / products_articles.amount)) as stock
    FROM
        products_articles
        LEFT JOIN (
            SELECT
                SUM("value") AS in_stock,
                article_id
            FROM
                stock_updates
            GROUP BY
                article_id) AS in_stock ON in_stock.article_id = products_articles.article_id
        JOIN products ON products_articles.product_id = products.product_id
    GROUP BY
        products_articles.product_id, products.name;
    """
    with SESSION_FACTORY() as session:
        result = session.execute(statement)
    return [ProductStock(*row) for row in result]
