DB_USER = "postgres"
DB_PASSWORD = "root"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_DATABASE = "testing_finance_app"

db_string = "postgresql://" + DB_USER + ":" + DB_PASSWORD + \
            "@" + DB_HOST + \
            ":" + DB_PORT + \
            "/" + DB_DATABASE
