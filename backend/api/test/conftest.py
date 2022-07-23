import pytest
from alembic.command import upgrade as alembic_upgrade, downgrade as alembic_downgrade
from alembic.config import Config as AlembicConfig

from api.persistence.connection import SESSION_FACTORY

alembic_config = AlembicConfig("alembic.ini")


@pytest.fixture(autouse=False)
def database():
    """Fixture for setting up database for test
    @TODO - recreation is not optimal, implement creating database in first test, and truncating tables between tests
    """
    alembic_downgrade(alembic_config, "base")
    alembic_upgrade(alembic_config, "head")
    yield None


@pytest.fixture(autouse=False)
def session():
    """Fixture giving access to session"""
    session = SESSION_FACTORY()
    yield session
    session.close()


@pytest.fixture(autouse=False)
def dump_table(session):
    """Fixture giving access to callable that returns all contents of given table"""

    def _run(table):
        # Sort by all columns for deterministic output
        return session.query(table).order_by(*table.columns).all()

    yield _run


@pytest.fixture(autouse=False)
def example_import_data():
    """Fixture providing data structured in import format"""
    return {
        "inventory": [
            {"art_id": "1", "name": "leg", "stock": "12"},
            {"art_id": "2", "name": "screw", "stock": "17"},
            {"art_id": "3", "name": "seat", "stock": "2"},
            {"art_id": "4", "name": "table top", "stock": "1"},
        ],
        "products": [
            {
                "name": "Dining Chair",
                "contain_articles": [
                    {"art_id": "1", "amount_of": "4"},
                    {"art_id": "2", "amount_of": "8"},
                    {"art_id": "3", "amount_of": "1"},
                ],
            },
            {
                "name": "Dinning Table",
                "contain_articles": [
                    {"art_id": "1", "amount_of": "4"},
                    {"art_id": "2", "amount_of": "8"},
                    {"art_id": "4", "amount_of": "1"},
                ],
            },
        ],
    }
