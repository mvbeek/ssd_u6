import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

VALUE_ERROR_MSG = "No {} set for the Env Variable. Go to README for more info."

# Database Configuration
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

if not DATABASE_USER:
    raise ValueError(VALUE_ERROR_MSG.format("DATABASE_USER"))
if not DATABASE_PASSWORD:
    raise ValueError(VALUE_ERROR_MSG.format("DATABASE_PASSWORD"))
if not DATABASE_HOST:
    raise ValueError(VALUE_ERROR_MSG.format("DATABASE_HOST"))
# if not DATABASE_PORT:
#     raise ValueError(VALUE_ERROR_MSG.format("DATABASE_PORT"))
if not DATABASE_NAME:
    raise ValueError(VALUE_ERROR_MSG.format("DATABASE_NAME"))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' \
                            + DATABASE_USER+':' \
                            + DATABASE_PASSWORD+'@' \
                            + DATABASE_HOST+'/' \
                            + DATABASE_NAME


# PyMySQL
engine = create_engine(SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    # import models
    Base.metadata.create_all(bind=engine)
