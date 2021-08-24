import praw
import config
import requests
from db.mention_repository import MentionRepository
from db.stock_repository import StockRepository
from base_db import Stock


class RedditScraper:
    """
    Uses praw to scrape data from reddit. Calls DB interface to store
    data into the database.

    === Public attributes ===
    reddit: an authorized reddit instance which is used to retrieve data
            from reddit
    """

    def __init__(self):
        self.r = praw.Reddit(
            client_id=config.client_id,
            client_secret=config.client_secret,
            password=config.password,
            user_agent=config.user_agent,
            username=config.username
        )

    def scrape(self):
        pass


class StockScraper:
    """
    Scrape stock and stock name to populate the stocks table in the database.

    === Private Attributes ===
    _stock_repository: a StockRepository instance

    """
    def __init__(self):
        self._stock_repository = StockRepository()

    def scrape(self) -> None:
        """
        Gets stock data from online and populate the stock table in the database by calling a DB function.
        """
        response = requests.get("http://ftp.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt")

        stocks = response.text.splitlines()
        for i in range(1, len(stocks)):
            stock_info = [info.strip() for info in stocks[i].split("|")]

            # only populate the stock table if it is not an etf
            if stock_info[4] == "N":
                if stock_info[2] == "A":
                    exchange = "NYSE MKT"
                elif stock_info[2] == "N":
                    exchange = "NYSE"
                elif stock_info[2] == "P":
                    exchange = "NYSE ARCA"
                elif stock_info[2] == "Z":
                    exchange = "BATS"
                else:
                    exchange = "IEXG"
                new_stock = Stock(symbol=stock_info[0], name=stock_info[1], exchange=exchange)
                self._stock_repository.input_stock(new_stock)


if __name__ == "__main__":
    scraper = StockScraper()
    scraper.scrape()
