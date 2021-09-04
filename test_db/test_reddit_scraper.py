from base_test_db import engine
from reddit_scraper import RedditScraper


def test_count_mention():
    scraper = RedditScraper("wallstreetbets", engine)
    scraper.count_mentions_and_populate_table("This was exactly me 2 weeks ago. Loaded my IRA up with GME. "
                                              "It dropped 6% no more than 10 min after I bought em’ all. "
                                              "A few days later, was up 25%. Still holding, and hoping the same "
                                              "gains for you!",
                                              "2020-08-30 8:30 PM",
                                              "eitlom",
                                              False)

test_count_mention()
