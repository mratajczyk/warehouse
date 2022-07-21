import hashlib
from typing import Tuple, List

from api.schemas.internal import Article, Product, ProductArticle, StockUpdate


def _hash_name(value: str) -> int:
    """Helper for hashing product names"""
    return int.from_bytes(
        bytes.fromhex(hashlib.md5(value.encode()).hexdigest()[:16]),
        "little",
        signed=True,
    )


def transform_import_data(
    json_content: dict,
) -> Tuple[List[Article], List[Product], List[ProductArticle], List[StockUpdate]]:
    """Transform incoming data to internal representations."""

    articles = []
    products = []
    stock_updates = []
    products_articles = []

    for item in json_content.get("inventory", []):
        articles.append(Article(article_id=int(item["art_id"]), name=item["name"]))
        stock_updates.append(
            StockUpdate(article_id=int(item["art_id"]), current=int(item["stock"]))
        )

    for product in json_content.get("products", []):
        product_id = _hash_name(product["name"])
        products.append(Product(product_id=product_id, name=product["name"]))
        for article_relation in product["contain_articles"]:
            products_articles.append(
                ProductArticle(
                    product_id=product_id,
                    article_id=int(article_relation["art_id"]),
                    amount=int(article_relation["amount_of"]),
                )
            )

    return articles, products, products_articles, stock_updates
