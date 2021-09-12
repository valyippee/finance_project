import logging
from typing import Optional, List
from base_db import engine, Mention
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import FlushError, ConcurrentModificationError


logger = logging.getLogger(__name__)


class MentionRepository:
    """
    Manages interaction with the mention table in the database.
    """
    def __init__(self, init_engine=engine):
        self.engine = init_engine

    def find_by_mention_id(self, _id: int) -> Optional[Mention]:
        """
        Returns a Mention that matches mention_id. If such mention does
        not exist, return None.
        """
        with Session(self.engine) as session:
            result = session.query(Mention).filter_by(mention_id=_id).all()
            return result[0]

    def filter_by_stock_and_dt(self, _id: int,
                               start: str, end: str) -> Optional[List[Mention]]:
        """
        Returns a list of all mention_id of mentions mentioning the stock
        that matches _id in the time frame given by start and end
        If the stock was never mentioned in the time frame, return None.
        Note: start and end are strings indicating timestamps and should be in
        the format of "%Y-%m-%d %H:%M:%S"
        """
        with Session(self.engine) as session:
            results = session.query(Mention).filter(Mention.stock_id == _id,
                                                    Mention.dt >= start,
                                                    Mention.dt <= end).all()
            result = [i.mention_id for i in results]
            return result

    def count_mention(self, ticker: int, start: str, end: str) -> int:
        """
        Returns the number of mentions that a stock have in the indicated
        timeframe.
        """
        mentions_lst = self.filter_by_stock_and_dt(ticker, start, end)
        if mentions_lst is not None:
            return len(mentions_lst)
        else:
            return 0

    def input_mention(self, new_mention: Mention) -> None:
        """
        Insert new_submission into the database.
        """
        with Session(self.engine) as session:
            try:
                session.add(new_mention)
                session.commit()
            except (SQLAlchemyError, FlushError, ConcurrentModificationError):
                session.rollback()
                raise
