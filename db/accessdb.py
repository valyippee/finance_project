import psycopg2
import psycopg2.extras
import config

CONNECTION = psycopg2.connect(database=config.DB_NAME,
                              user=config.DB_USER,
                              password=config.DB_NAME)


class DB:
    """
    In charge of interactions with the database
    """
    def __init__(self):
        self.cursor = CONNECTION.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def retrieve(self):
        pass

    def input(self):
        pass
