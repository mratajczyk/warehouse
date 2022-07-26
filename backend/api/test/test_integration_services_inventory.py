import datetime
from unittest.mock import Mock
from uuid import UUID

import pytest
from freezegun import freeze_time

from api.persistence.tables import articles as articles_table
from api.persistence.tables import products as products_table
from api.persistence.tables import products_articles as products_articles_table
from api.persistence.tables import stock_updates as stock_updates_table
from api.schemas.internal import (Article, ImportStockUpdate, Product,
                                  ProductArticle)
from api.services.inventory import (UpdateInventoryException,
                                    run_update_inventory, update_inventory)

insert_articles = [
    Article(article_id="1", name="Foo"),
    Article(article_id="2", name="Bar"),
    Article(article_id="3", name="FooBar"),
]


insert_products = [
    Product(product_id="1", name="Product1"),
    Product(product_id="2", name="Product2"),
    Product(product_id="3", name="Product3"),
]


expected_articles = [("1", "Foo"), ("2", "Bar"), ("3", "FooBar")]
expected_products = [("1", "Product1"), ("2", "Product2"), ("3", "Product3")]


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
    update_inventory(articles, products, [], [])

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
        Article(article_id="1", name="Foo"),
        Article(article_id="2", name="Bar"),
        Article(article_id="3", name="FooBar"),
    ]
    products = [
        Product(
            product_id="1",
            name="Product1",
        ),
        Product(
            product_id="2",
            name="Product2",
        ),
    ]

    products_articles = [
        ProductArticle(product_id="1", article_id="1", amount=111),
        ProductArticle(product_id="1", article_id="2", amount=222),
        ProductArticle(product_id="2", article_id="2", amount=444),
    ]

    update_inventory(articles, products, products_articles, [])
    inserted_products_articles = dump_table(products_articles_table)

    assert inserted_products_articles == [
        ("1", "1", 111),
        ("1", "2", 222),
        ("2", "2", 444),
    ]


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
                ProductArticle(product_id="1", article_id="1", amount=111),
            ],
            [],
        )


def test_run_update_inventory(
    database, session, dump_table, example_import_data, mocker
):
    """
    GIVEN run_update_inventory functions
    WHEN updating inventory using data coming from import
    THEN check if inventory was created properly in database
    """
    mocker.patch(
        "api.services.prepare_import.uuid.uuid4",
        Mock(
            side_effect=[
                UUID("75138e7b-37ac-436e-a403-e0bac1294c2b"),
                UUID("d9b7e54a-6ed6-45e1-9a47-8ff3979ea000"),
                UUID("ec2b035e-6cae-46e1-bd75-451f81236155"),
                UUID("f7055876-aae9-46e1-9b7a-6c193d47408b"),
            ]
        ),
    )

    with freeze_time("2022-01-01"):
        run_update_inventory(example_import_data)

    inserted_articles = dump_table(articles_table)
    inserted_products = dump_table(products_table)
    inserted_products_articles = dump_table(products_articles_table)
    inserted_stock_updates = dump_table(stock_updates_table)

    assert (
        inserted_articles,
        inserted_products,
        inserted_products_articles,
        inserted_stock_updates,
    ) == (
        [("1", "leg"), ("2", "screw"), ("3", "seat"), ("4", "table top")],
        [
            ("2582353817615226871", "Dinning Table"),
            ("8554657820763869416", "Dining Chair"),
        ],
        [
            ("2582353817615226871", "1", 4),
            ("2582353817615226871", "2", 8),
            ("2582353817615226871", "4", 1),
            ("8554657820763869416", "1", 4),
            ("8554657820763869416", "2", 8),
            ("8554657820763869416", "3", 1),
        ],
        [
            (
                UUID("75138e7b-37ac-436e-a403-e0bac1294c2b"),
                "1",
                None,
                12,
                datetime.datetime(2022, 1, 1, 0, 0),
            ),
            (
                UUID("d9b7e54a-6ed6-45e1-9a47-8ff3979ea000"),
                "2",
                None,
                17,
                datetime.datetime(2022, 1, 1, 0, 0),
            ),
            (
                UUID("ec2b035e-6cae-46e1-bd75-451f81236155"),
                "3",
                None,
                2,
                datetime.datetime(2022, 1, 1, 0, 0),
            ),
            (
                UUID("f7055876-aae9-46e1-9b7a-6c193d47408b"),
                "4",
                None,
                1,
                datetime.datetime(2022, 1, 1, 0, 0),
            ),
        ],
    )


def test_update_stock_updates(database, session, dump_table, mocker):
    """
    GIVEN update function for setting current inventory state
    WHEN calling function and inserting Stock Updates
    THEN check if Stock Updates were persisted properly
    """
    mocker.patch(
        "api.services.inventory.get_stocks_for_articles", Mock(return_value={"4": 5})
    )
    mocker.patch(
        "api.services.prepare_import.uuid.uuid4",
        Mock(
            side_effect=[
                UUID("75138e7b-37ac-436e-a403-e0bac1294c2b"),
                UUID("d9b7e54a-6ed6-45e1-9a47-8ff3979ea000"),
                UUID("ec2b035e-6cae-46e1-bd75-451f81236155"),
                UUID("f7055876-aae9-46e1-9b7a-6c193d47408b"),
            ]
        ),
    )
    articles = [
        Article(article_id="1", name="Foo"),
        Article(article_id="2", name="Bar"),
        Article(article_id="3", name="FooBar"),
        Article(article_id="4", name="FooBar4"),
    ]
    with freeze_time("2022-01-01"):
        update_inventory(
            articles,
            [],
            [],
            [
                ImportStockUpdate(article_id="1", current=100),
                ImportStockUpdate(article_id="2", current=200),
                ImportStockUpdate(article_id="3", current=300),
                ImportStockUpdate(article_id="4", current=0),
            ],
        )
    assert dump_table(stock_updates_table) == [
        (
            UUID("75138e7b-37ac-436e-a403-e0bac1294c2b"),
            "1",
            None,
            100,
            datetime.datetime(2022, 1, 1, 0, 0),
        ),
        (
            UUID("d9b7e54a-6ed6-45e1-9a47-8ff3979ea000"),
            "2",
            None,
            200,
            datetime.datetime(2022, 1, 1, 0, 0),
        ),
        (
            UUID("ec2b035e-6cae-46e1-bd75-451f81236155"),
            "3",
            None,
            300,
            datetime.datetime(2022, 1, 1, 0, 0),
        ),
        (
            UUID("f7055876-aae9-46e1-9b7a-6c193d47408b"),
            "4",
            None,
            -5,
            datetime.datetime(2022, 1, 1, 0, 0),
        ),
    ]
