from datetime import datetime
from typing import Optional, TypedDict
from uuid import UUID

"""
List of internal data structures.

@TODO - consider using immutable type like frozen dataclass
"""


class Article(TypedDict):
    article_id: str
    name: str


class ProductArticle(TypedDict):
    product_id: str
    article_id: str
    amount: int


class Product(TypedDict):
    product_id: str
    name: str


class ImportStockUpdate(TypedDict):
    article_id: str
    current: int


class StockUpdate(TypedDict):
    update_id: UUID
    article_id: str
    value: int
    created_at: datetime
    sale_id: Optional[UUID]


class Sale(TypedDict):
    sale_id: UUID
    product_id: str
    amount: int
