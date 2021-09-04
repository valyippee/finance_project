import logging.config
import yaml
import os
from reddit_scraper import RedditScraper

log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep + os.pardir), 'logs')
log_fname = os.path.join(log_dir, 'output.log')
log_config_fname = os.path.join(log_dir, 'logging_config.yaml')

with open(log_config_fname, 'r') as f:
    config = yaml.safe_load(f.read())
    config['handlers']['file']['filename'] = log_fname
    logging.config.dictConfig(config)

# from base_test_db import engine
# from reddit_scraper import RedditScraper
#
#
# def test_count_mention():
#     scraper = RedditScraper("wallstreetbets", engine)
#     scraper.count_mentions_and_populate_table("This was exactly me 2 weeks ago. Loaded my IRA up with GME. "
#                                               "It dropped 6% no more than 10 min after I bought em’ all. "
#                                               "A few days later, was up 25%. Still holding, and hoping the same "
#                                               "gains for you!",
#                                               "2020-08-30 8:30 PM",
#                                               "eitlom",
#                                               False)
#
# test_count_mention()