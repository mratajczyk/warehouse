from api.services.stocks import get_stocks_for_articles


def test_get_stocks_for_articles(database, session, set_example_database_sale):
    """
    GIVEN get_stocks_for_articles function
    WHEN calling it with list of article_id's
    THEN check if proper result is returned for articles set up in fixture
    """
    assert get_stocks_for_articles(session, [1, 2, 3]) == {1: 5, 2: 3, 3: 1}
