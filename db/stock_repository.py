from typing import List, Optional

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
        Inputs stock into stock table.

        Precondition: this stock belongs to a company, not an etf.
        """
        with self.Session() as session:
            session.add(new_stock)
            session.commit()

    def find_by_id(self, stock_id: int) -> Optional[Stock]:
        """
        Returns a Stock based on id, or None if the stock does not exist.
        """
        session = self.Session()
        result = session.query(Stock).get(stock_id)
        session.close()
        return result

    def find_all(self) -> List[Stock]:
        """
        Returns all Stock in the database in a list.
        """
        session = self.Session()
        result = session.query(Stock).all()
        session.close()
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
