import uuid
from datetime import datetime
from unittest.mock import Mock
from uuid import UUID

import pytest
from freezegun import freeze_time

from api.persistence.tables import sales as sales_table
from api.persistence.tables import stock_updates as stock_updates_table
from api.services.sales import ProductNotFound, register_sale


def test_register_sale(
    database, set_example_database_products_articles, dump_table, mocker
):
    """
    GIVEN register_sale function
    WHEN calling arguments for Product and amount
    THEN check if sale have been properly persisted
    """
    sale_id = uuid.uuid4()
    mocker.patch("api.services.sales._generate_sale_id", Mock(return_value=sale_id))
    mocker.patch(
        "api.services.sales.uuid.uuid4",
        Mock(
            side_effect=[
                UUID("1060d9a7-ea4e-4235-9518-bbf888387694"),
                UUID("bf881d67-bb22-4f1c-89ab-64ca4966f631"),
                UUID("d7045697-530c-4a0d-a05a-19336734481e"),
            ]
        ),
    )

    with freeze_time("2022-01-01"):
        register_sale("1", 1)

    assert dump_table(sales_table), dump_table(stock_updates_table) == (
        [(sale_id, "1", 1)],
        [
            (
                UUID("1060d9a7-ea4e-4235-9518-bbf888387694"),
                "3",
                sale_id,
                -1,
                datetime.datetime(2022, 1, 1, 0, 0),
            ),
            (
                UUID("bf881d67-bb22-4f1c-89ab-64ca4966f631"),
                "2",
                sale_id,
                -8,
                datetime.datetime(2022, 1, 1, 0, 0),
            ),
            (
                UUID("d7045697-530c-4a0d-a05a-19336734481e"),
                "1",
                sale_id,
                -4,
                datetime.datetime(2022, 1, 1, 0, 0),
            ),
        ],
    )


@pytest.mark.parametrize(
    "inputs, exception",
    [
        # Invalid amount
        (("1", 0), ValueError),
        (("1", -1), ValueError),
        # Not existing Product
        (("999", 1), ProductNotFound),
    ],
)
def test_register_sale_invalid(
    database, set_example_database_products_articles, inputs, exception
):
    """
    GIVEN register_sale function
    WHEN calling with invalid arguments
    THEN check if proper execution is raised
    """
    with pytest.raises(exception):
        register_sale(*inputs)
