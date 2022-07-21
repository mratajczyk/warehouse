from typing import TypedDict, List


class Article(TypedDict):
    article_id: int
    name: str


class ProductArticle(TypedDict):
    product_id: int
    article_id: int
    amount: int


class Product(TypedDict):
    product_id: int
    name: str


class StockUpdate(TypedDict):
    article_id: int
    current: int
