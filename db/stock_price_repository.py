from typing import Optional

from base_db import engine, DailyStockPrice
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import FlushError, ConcurrentModificationError
import logging

logger = logging.getLogger(__name__)


class DailyStockPriceRepository:
    """
    Manages the interactions with the stock_price table in the database
    """

    def __init__(self, init_engine=engine):
        """
        Defines an instance of Stock_price _repository to interact with the
        stock_price table in the database. The default engine is the engine
        from base_db that is connected to Finance_App_db in PostgreSQL.
        """
        self.engine = init_engine

    def input_prices(self, stock_prices: DailyStockPrice) -> None:
        """
        Inputs the OHLC, datetime, volume of a stock into the database table
        """
        with Session(self.engine) as session:
            try:
                session.add(stock_prices)
                session.flush()
                session.commit()
            except (SQLAlchemyError, FlushError, ConcurrentModificationError):
                session.rollback()
                raise

    def find_price_by_id_dt(self, ticker: str,
                            start: str, end: str, ohlc: str) -> Optional[dict]:
        """
        Return a dictionary containing the OHLC prices of the indicated
        stock from start to end with the key being the date and the value being
        the price. Return an empty dictionary if no data found.
        """
        with Session(self.engine) as session:
            result = {}
            results = session.query(DailyStockPrice).filter(
                                            DailyStockPrice.stock_id == ticker,
                                            DailyStockPrice.dt >= start,
                                            DailyStockPrice.dt <= end).all()
            for row in results:
                if ohlc == "O":
                    result[row.dt] = row.open
                elif ohlc == "H":
                    result[row.dt] = row.high
                elif ohlc == "L":
                    result[row.dt] = row.low
                elif ohlc == "C":
                    result[row.dt] = row.close
            return result


