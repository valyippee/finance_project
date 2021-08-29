"""
Contains the module/ application level attributes of sqlalchemy which all repositories and functions will reference.
"""


from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
import db.config as config

engine = create_engine(config.db_string)

Base = declarative_base()
AutoBase = automap_base()
AutoBase.prepare(engine, reflect=True)

Stock = AutoBase.classes.stock
StockPrice = AutoBase.classes.stock_price
Mention = AutoBase.classes.mention
Comment = AutoBase.classes.comment
Submission = AutoBase.classes.submission

