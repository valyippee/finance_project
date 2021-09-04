from typing import List, Optional

from base_db import engine, Stock
from sqlalchemy.orm import sessionmaker
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import FlushError, ConcurrentModificationError

logger = logging.getLogger(__name__)


class StockRepository:
    """
    Manages interaction with the stock table in the database.
    """

    def __init__(self, init_engine=engine):
        """
        Initializes the StockRepository with a default engine imported from base_db.
        """
        self.Session = sessionmaker(init_engine)

    def input_stock(self, new_stock: Stock):
        """
        Inputs stock into stock table.

        Precondition: this stock belongs to a company, not an etf.
        """
        with self.Session() as session:
            try:
                session.add(new_stock)
                session.commit()
            except (SQLAlchemyError, FlushError, ConcurrentModificationError):
                session.rollback()
                raise

    def find_by_id(self, stock_id: int) -> Optional[Stock]:
        """
        Returns a Stock based on id, or None if the stock does not exist.
        """
        with self.Session() as session:
            result = session.query(Stock).get(stock_id)
        return result

    def find_by_ticker(self, ticker: str) -> Optional[Stock]:
        """
        Returns a Stock based on ticker, or None if the stock does not exist.
        """
        with self.Session() as session:
            result = session.query(Stock).filter(Stock.symbol == ticker).first()
        return result

    def find_all(self) -> List[Stock]:
        """
        Returns all Stock in the database in a list.
        """
        with self.Session() as session:
            result = session.query(Stock).all()
        return result

    def find_all_name_variations(self):
        """
        Returns all name_variations of all stocks in the database
        """
        with self.Session() as session:
            result = session.query(Stock.name_variations).all()
        return result

    def delete_by_id(self, stock_id: int) -> None:
        """
        Deletes a Stock based on id, if the Stock is in the database.
        Deletes data from other tables as well to maintain foreign key constraint.
        """
        with self.Session() as session:
            session.query(Stock).filter(Stock.id == stock_id).delete()
            session.commit()

    def delete_all(self) -> None:
        """
        Deletes all Stock in the database
        Deletes data from other tables as well to maintain foreign key constraint.
        """
        with self.Session() as session:
            session.query(Stock).delete()
            session.commit()
