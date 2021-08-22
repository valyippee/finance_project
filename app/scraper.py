import praw
import config


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
    """
    def __init__(self):
        pass

    def scrape(self):
        pass
