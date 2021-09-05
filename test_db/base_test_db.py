"""
Contains the module/ application level attributes of sqlalchemy which all repositories and functions will reference.
"""


from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
import test_db.test_config as test_config

engine = create_engine(test_config.db_string)

Base = declarative_base()
AutoBase = automap_base()
AutoBase.prepare(engine, reflect=True)

Stock = AutoBase.classes.stock
