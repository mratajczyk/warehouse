from datetime import datetime
from typing import List, Optional, TypedDict
from uuid import UUID


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


class ImportStockUpdate(TypedDict):
    article_id: int
    current: int


class StockUpdate(TypedDict):
    update_id: UUID
    article_id: int
    value: int
    created_at: datetime
    sale_id: Optional[UUID]


class Sale(TypedDict):
    sale_id: UUID
    product_id: int
    amount: int
