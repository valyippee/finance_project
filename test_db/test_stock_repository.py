"""
Test each function from StockRepository
"""

from db.stock_repository import StockRepository
from test_db.base_test_db import Stock, engine


def test_input_stock():
    stock_repository = StockRepository(engine)
    sample_stock = Stock(symbol="234", name="sample2", exchange="NYSE")
    stock_repository.input_stock(sample_stock)


def test_find_stock_by_id():
    stock_repository = StockRepository(engine)
    returned_stock = stock_repository.find_by_id(1)
    print(returned_stock.name_variations)


def test_find_all():
    stock_repository = StockRepository(engine)
    result = stock_repository.find_all()
    for stock in result:
        print(stock.id)


def test_find_by_ticker():
    stock_repository = StockRepository()
    result = stock_repository.find_by_ticker("AA")
    print(str(result))
    print(type(result))

    result2 = stock_repository.find_by_ticker("123")
    assert result2 is None


def test_delete_by_id():
    stock_repository = StockRepository(engine)
    stock_repository.delete_by_id(2)
    print(stock_repository.find_by_id(2))


def test_delete_all():
    stock_repository = StockRepository(engine)
    assert stock_repository.find_all() is None


test_find_by_ticker()
