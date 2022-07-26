import datetime
import hashlib
import sys
import uuid
from typing import List, Tuple

from api.schemas.internal import (
    Article,
    ImportStockUpdate,
    Product,
    ProductArticle,
    StockUpdate,
)


def _hash_name(value: str) -> str:
    """Helper for hashing product to numeric string"""
    return str(
        int.from_bytes(
            bytes.fromhex(hashlib.md5(value.encode()).hexdigest()[:16]),
            sys.byteorder,
            signed=True,
        )
    )


def get_stock_updates(article_stocks: dict, import_state: List[ImportStockUpdate]):
    """Function preparing StockUpdates for database insertion based on current Article Stocks adn data from import"""
    return [
        StockUpdate(
            value=state["current"] - article_stocks.get(state["article_id"], 0),
            update_id=uuid.uuid4(),
            article_id=state["article_id"],
            created_at=datetime.datetime.now(),
            sale_id=None,
        )
        for state in import_state
    ]


def transform_import_data(
    json_content: dict,
) -> Tuple[List[Article], List[Product], List[ProductArticle], List[ImportStockUpdate]]:
    """Transform incoming data to internal representations."""
    articles = []
    products = []
    stock_updates = []
    products_articles = []

    for item in json_content.get("inventory", []):
        articles.append(Article(article_id=item["article_id"], name=item["name"]))
        stock_updates.append(
            ImportStockUpdate(article_id=item["article_id"], current=item["stock"])
        )

    for product in json_content.get("products", []):
        product_id = _hash_name(product["name"])
        products.append(Product(product_id=product_id, name=product["name"]))
        for article_relation in product["contain_articles"]:
            products_articles.append(
                ProductArticle(
                    product_id=product_id,
                    article_id=article_relation["article_id"],
                    amount=article_relation["amount"],
                )
            )

    return articles, products, products_articles, stock_updates
