import logging.config
import yaml
import os
from base_test_db import engine
from reddit_scraper import RedditScraper

log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep + os.pardir), 'logs')
log_fname = os.path.join(log_dir, 'output.log')
log_config_fname = os.path.join(log_dir, 'logging_config.yaml')

with open(log_config_fname, 'r') as f:
    config = yaml.safe_load(f.read())
    config['handlers']['file']['filename'] = log_fname
    logging.config.dictConfig(config)


scraper = RedditScraper("wallstreetbets", engine)

scraper.get_live_comments()