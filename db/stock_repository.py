import psycopg2
import psycopg2.extras
import db.config as config

CONNECTION = psycopg2.connect(database=config.DB_NAME,
                              user=config.DB_USER,
                              password=config.DB_PASSWORD)


class StockRepository:
    """
    Manages interaction with the stock table in the database.
    """

    def __init__(self):
        self.cursor = CONNECTION.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def input_stock(self, ticker: str, company_name: str, exchange: str):
        """
        Inputs stock into stock table

        Precondition: this stock belongs to a company, not an etf
        """
        pass
