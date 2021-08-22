import psycopg2
import psycopg2.extras
import db.config as config

CONNECTION = psycopg2.connect(database=config.DB_NAME,
                              user=config.DB_USER,
                              password=config.DB_PASSWORD)


class MentionRepository:
    """
    In charge of interactions with the database
    """
    def __init__(self):
        self.cursor = CONNECTION.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def retrieve(self):
        pass

    def input(self):
        pass
