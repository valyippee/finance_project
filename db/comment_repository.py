import psycopg2
import psycopg2.extras
import db.config as config

CONNECTION = psycopg2.connect(database=config.DB_NAME,
                              user=config.DB_USER,
                              password=config.DB_PASSWORD)