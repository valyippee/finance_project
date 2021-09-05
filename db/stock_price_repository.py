from base_db import engine, StockPrice
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import FlushError, ConcurrentModificationError
import logging

logger = logging.getLogger(__name__)


class Stock_price_repository:
    """
    Manages the interactions with the stock_price table in the database
    """
    def __init__(self, initengine = engine):
        """
        Defines an instance of Stock_price _repository to interact with the
        stock_price table in the database. The default engine is the engine
        from base_db that is connected to Finance_App_db in PostgreSQL.
        """
        self.engine = initengine

    def input_prices(self, stock_prices: StockPrice):
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

    def delect_prices_by_id_dt(self, stock_prices: StockPrice):
        """
        Delete a row in the stock_price table by id and dt
        """
        with Session(self.engine) as session:
            pass

    def find_data(self













