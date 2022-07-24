from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import functions as func

from api.persistence.tables import stock_updates


def get_stocks_for_articles(session: Session, article_id: List[int]) -> dict:
    """Returns current stock for given articles in form of dictionary where key is article_id"""
    statement = (
        select([stock_updates.c.article_id, func.sum(stock_updates.c.value)])
        .group_by(stock_updates.c.article_id)
        .where(stock_updates.c.article_id.in_(article_id))
    )
    return {row[0]: row[1] for row in session.execute(statement).all()}
