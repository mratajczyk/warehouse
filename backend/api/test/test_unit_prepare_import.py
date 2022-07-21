from api.services.perpare_import import transform_import_data


def test_transform_import_data(example_import_data):
    """
    GIVEN transform_import_data function
    WHEN calling it with valid input representing warehouse inventory
    THEN check if proper local representations are returned
    """

    assert transform_import_data(example_import_data) == (
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
