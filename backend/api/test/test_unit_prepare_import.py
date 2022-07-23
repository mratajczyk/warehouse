import pytest
from marshmallow import ValidationError

from api.services.inventory import deserialize_incoming_data
from api.services.perpare_import import transform_import_data

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
    [{}, {"products": [], "inventory": []}],
)
def test_deserialize_incoming_data_validation_export(invalid_input):
    """
    GIVEN deserialize_incoming_data function
    WHEN calling it with invalid data from import file
    THEN check if proper local representations are returned
    """
    with pytest.raises(ValidationError):
        deserialize_incoming_data(invalid_input)
