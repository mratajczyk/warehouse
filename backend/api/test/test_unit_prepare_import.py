from datetime import datetime
from unittest.mock import Mock

import pytest
from marshmallow import ValidationError

from api.schemas.internal import ImportStockUpdate
from api.services.inventory import deserialize_incoming_data
from api.services.prepare_import import transform_import_data, get_stock_updates

loaded_import_data = {
    "inventory": [
        {"name": "leg", "article_id": 1.0, "stock": 12.0},
        {"name": "screw", "article_id": 2.0, "stock": 17.0},
        {"name": "seat", "article_id": 3.0, "stock": 2.0},
        {"name": "table top", "article_id": 4.0, "stock": 1.0},
    ],
    "products": [
        {
            "name": "Dining Chair",
            "contain_articles": [
                {"article_id": 1.0, "amount": 4.0},
                {"article_id": 2.0, "amount": 8.0},
                {"article_id": 3.0, "amount": 1.0},
            ],
        },
        {
            "name": "Dinning Table",
            "contain_articles": [
                {"article_id": 1.0, "amount": 4.0},
                {"article_id": 2.0, "amount": 8.0},
                {"article_id": 4.0, "amount": 1.0},
            ],
        },
    ],
}


def test_transform_import_data():
    """
    GIVEN transform_import_data function
    WHEN calling it with valid input representing warehouse inventory
    THEN check if proper local representations are returned
    """
    assert transform_import_data(loaded_import_data) == (
        [
            {"article_id": 1, "name": "leg"},
            {"article_id": 2, "name": "screw"},
            {"article_id": 3, "name": "seat"},
            {"article_id": 4, "name": "table top"},
        ],
        [
            {"product_id": 8554657820763869416, "name": "Dining Chair"},
            {"product_id": 2582353817615226871, "name": "Dinning Table"},
        ],
        [
            {"product_id": 8554657820763869416, "article_id": 1, "amount": 4},
            {"product_id": 8554657820763869416, "article_id": 2, "amount": 8},
            {"product_id": 8554657820763869416, "article_id": 3, "amount": 1},
            {"product_id": 2582353817615226871, "article_id": 1, "amount": 4},
            {"product_id": 2582353817615226871, "article_id": 2, "amount": 8},
            {"product_id": 2582353817615226871, "article_id": 4, "amount": 1},
        ],
        [
            {"article_id": 1, "current": 12},
            {"article_id": 2, "current": 17},
            {"article_id": 3, "current": 2},
            {"article_id": 4, "current": 1},
        ],
    )


def test_deserialize_incoming_data(example_import_data):
    """
    GIVEN deserialize_incoming_data function
    WHEN calling it with data from import file
    THEN check if proper local representations are returned
    """
    assert deserialize_incoming_data(example_import_data) == loaded_import_data


@pytest.mark.parametrize(
    "invalid_input",
    [{"products": ["Foo"], "inventory": []}, {"products": [], "inventory": ["Bar"]}],
)
def test_deserialize_incoming_data_validation_export(invalid_input):
    """
    GIVEN deserialize_incoming_data function
    WHEN calling it with invalid data from import file
    THEN check if proper local representations are returned
    """
    with pytest.raises(ValidationError):
        deserialize_incoming_data(invalid_input)


@pytest.mark.freeze_time("2022-01-01")
def test_get_stock_updates(mocker):
    """
    GIVEN get_stock_updates function
    WHEN calling it with current stocks and values coming from import
    THEN check returned updates for database are correct
    """
    mocker.patch(
        "api.services.prepare_import.uuid.uuid4", Mock(return_value="mocked-uuid")
    )
    current = {1: 100, 2: 200, 3: 300}
    import_state = [
        ImportStockUpdate(article_id=1, current=200),
        ImportStockUpdate(article_id=2, current=50),
        ImportStockUpdate(article_id=3, current=300),
    ]
    assert get_stock_updates(current, import_state) == [
        {
            "value": 100,
            "update_id": "mocked-uuid",
            "article_id": 1,
            "created_at": datetime(2022, 1, 1, 0, 0),
            "sale_id": None,
        },
        {
            "value": -150,
            "update_id": "mocked-uuid",
            "article_id": 2,
            "created_at": datetime(2022, 1, 1, 0, 0),
            "sale_id": None,
        },
        {
            "value": 0,
            "update_id": "mocked-uuid",
            "article_id": 3,
            "created_at": datetime(2022, 1, 1, 0, 0),
            "sale_id": None,
        },
    ]
