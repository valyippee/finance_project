"""
Contains the module/ application level attributes of sqlalchemy which all repositories and functions will reference.
"""


from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import db.config as config

engine = create_engine(config.db_string)
Session = sessionmaker(bind=engine)

Base = declarative_base()
AutoBase = automap_base()
AutoBase.prepare(engine, reflect=True)

Stock = AutoBase.classes.stock
