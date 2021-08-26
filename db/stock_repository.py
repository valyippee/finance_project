from base_db import engine, Stock
from sqlalchemy.orm import sessionmaker


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
        Inputs stock into stock table

        Precondition: this stock belongs to a company, not an etf
        """
        with self.Session() as session:
            session.add(new_stock)
            session.commit()
