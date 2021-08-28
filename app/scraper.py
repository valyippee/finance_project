from typing import List

import praw
import config
import requests
from db.mention_repository import MentionRepository
from db.stock_repository import StockRepository
from base_db import Stock


LEGAL_ELEMENTS = ["Ltd.", "Corp.", "Corp", "Corporation", "Inc.", "Inc", "Incorporated", "Plc"]
TO_DELETE = ["Services", "Capital", "Holdings", "Holding", "Investment Trust",
             "Realty Trust", "Property Trust", "Properties Trust"]
TO_DELETE2 = ["Hotels & Resorts", "Systems", "Properties", "Technologies", "Group"]


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

                # filter out name_variations of the stock
                name_variations = [stock_info[0], stock_info[1]]
                name_variations.extend(self._form_name_variations(stock_info[1]))

                new_stock = Stock(symbol=stock_info[0],
                                  name=stock_info[1],
                                  exchange=exchange,
                                  name_variations=name_variations)
                self._stock_repository.input_stock(new_stock)

    def _form_name_variations(self, company_name: str) -> List:
        """
        Given a company's name, return a list of name variations to be stored in the database.
        """
        name_variations = []
        shortform_name = ""
        for element in LEGAL_ELEMENTS:
            if element in company_name:
                name_parts = company_name.split(element)
                shortform_name = name_parts[0].strip()
                if len(shortform_name) > 0 and shortform_name[-1] == ",":
                    shortform_name = shortform_name[0:len(shortform_name) - 1]
                break
        if shortform_name == "":
            return []
        else:
            name_variations.append(shortform_name)

        # further break down the names
        if "Technologies" in shortform_name:
            new_name = shortform_name.replace("Technologies", "Tech")
            name_variations.append(new_name)
        elif "Group" in shortform_name:
            new_name = shortform_name.replace("Group", "Grp")
            name_variations.append(new_name)
        elif "Hotels & Resorts" in shortform_name:
            new_name = shortform_name.replace("Hotels & Resorts", "Hotels")
            name_variations.append(new_name)

        for name_to_delete in TO_DELETE:
            if name_to_delete in shortform_name:
                new_name_parts = shortform_name.split(name_to_delete)
                name_variations.append(new_name_parts[0].strip())
        for name_to_delete in TO_DELETE2:
            if name_to_delete in shortform_name:
                new_name_parts = shortform_name.split(name_to_delete)
                name_variations.append(new_name_parts[0].strip())
        return name_variations


if __name__ == "__main__":
    scraper = StockScraper()
    scraper.scrape()