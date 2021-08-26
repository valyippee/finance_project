"""
Test each function from StockRepository
"""

from db.stock_repository import StockRepository
from test_db.base_test_db import Stock, engine


def test_input_stock():
    stock_repository = StockRepository(engine)
    sample_stock = Stock(symbol="123", name="sample", exchange="NYSE")
    stock_repository.input_stock(sample_stock)


test_input_stock()
