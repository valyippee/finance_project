from base_db import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer
from base_db import Base


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    name = Column(String)
    exchange = Column(String)


class StockRepository:
    """
    Manages interaction with the stock table in the database.
    """

    def __init__(self):
        Session = sessionmaker(engine)
        engine.connect()
        self.session = Session()

    def input_stock(self, new_stock: Stock):
        """
        Inputs stock into stock table

        Precondition: this stock belongs to a company, not an etf
        """
        self.session.add(new_stock)
        self.session.commit()


if __name__ == "__main__":
    stock_repository = StockRepository()
    sample_stock = Stock(symbol="123", name="sample", exchange="NYSE")
    stock_repository.input_stock(sample_stock)

