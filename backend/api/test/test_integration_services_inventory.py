import pytest

from api.schemas.internal import Article, Product, ProductArticle
from api.services.inventory import update_inventory, UpdateInventoryException

from api.persistence.tables import (
    products as products_table,
    articles as articles_table,
    products_articles as products_articles_table,
)
from api.services.perpare_import import transform_import_data

insert_articles = [
    Article(article_id=1, name="Foo"),
    Article(article_id=2, name="Bar"),
    Article(article_id=3, name="FooBar"),
]


insert_products = [
    Product(product_id=1, name="Product1"),
    Product(product_id=2, name="Product2"),
    Product(product_id=3, name="Product3"),
]


expected_articles = [(1, "Foo"), (2, "Bar"), (3, "FooBar")]
expected_products = [(1, "Product1"), (2, "Product2"), (3, "Product3")]


@pytest.mark.parametrize(
    "articles, products, result_articles, result_products",
    [
        (insert_articles, [], expected_articles, []),
        ([], insert_products, [], expected_products),
        (insert_articles, insert_products, expected_articles, expected_products),
    ],
)
def test_update(
    database,
    session,
    dump_table,
    articles,
    products,
    result_articles,
    result_products,
):
    """
    GIVEN update function for setting current inventory state
    WHEN calling function and inserting inventory to empty database
    THEN check if inventory was created properly
    """
    update_inventory(articles, products, [])

    inserted_articles = dump_table(articles_table)
    inserted_products = dump_table(products_table)

    assert (inserted_articles, inserted_products) == (
        result_articles,
        result_products,
    )


def test_update_product_contains(
    database,
    session,
    dump_table,
):
    """
    GIVEN update function for setting current inventory state
    WHEN calling function and inserting Products with defined relationships to Articles
    THEN check if inventory was persisted properly
    """
    articles = [
        Article(article_id=1, name="Foo"),
        Article(article_id=2, name="Bar"),
        Article(article_id=3, name="FooBar"),
    ]
    products = [
        Product(
            product_id=1,
            name="Product1",
        ),
        Product(
            product_id=2,
            name="Product2",
        ),
    ]

    products_articles = [
        ProductArticle(product_id=1, article_id=1, amount=111),
        ProductArticle(product_id=1, article_id=2, amount=222),
        ProductArticle(product_id=2, article_id=2, amount=444),
    ]

    update_inventory(articles, products, products_articles)
    inserted_products_articles = dump_table(products_articles_table)

    assert inserted_products_articles == [(1, 1, 111), (1, 2, 222), (2, 2, 444)]


def test_update_product_contains_exception(
    database,
    session,
    dump_table,
):
    """
    GIVEN update function for setting current inventory state
    WHEN calling function and inserting Products with incorrect relationships to Articles
    THEN check if exception is raised
    """
    with pytest.raises(UpdateInventoryException):
        update_inventory(
            [],
            [],
            [
                ProductArticle(product_id=1, article_id=1, amount=111),
            ],
        )


def test_update_on_import_data(database, session, dump_table, example_import_data):
    """
    GIVEN update_inventory and transform_import_data functions
    WHEN updating inventory using data coming from import
    THEN check if inventory was created properly in database
    """
    articles, products, products_articles, stock_updates = transform_import_data(
        example_import_data
    )

    update_inventory(articles, products, products_articles)

    inserted_articles = dump_table(articles_table)
    inserted_products = dump_table(products_table)
    inserted_products_articles = dump_table(products_articles_table)

    assert (inserted_articles, inserted_products, inserted_products_articles) == (
        [(1, "leg"), (2, "screw"), (3, "seat"), (4, "table top")],
        [(2582353817615226871, "Dinning Table"), (8554657820763869416, "Dining Chair")],
        [
            (2582353817615226871, 1, 4),
            (2582353817615226871, 2, 8),
            (2582353817615226871, 4, 1),
            (8554657820763869416, 1, 4),
            (8554657820763869416, 2, 8),
            (8554657820763869416, 3, 1),
        ],
    )
