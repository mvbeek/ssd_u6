'''
Any configuration that relates to the database.
It is required to store env variables in the server by
running `export ENV_VAR=value`.
e.g. `export DATABASE_USER=hogehoge`
'''
import os
from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

VALUE_ERROR_MSG = "No {} set for the Env Variable. Go to README for more info."

# Database Configuration
DATABASE_USER = os.environ.get("DATABASE_USER", 'root')
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", 'password')
DATABASE_HOST = os.environ.get("DATABASE_HOST", 'localhost')
DATABASE_PORT = os.environ.get("DATABASE_PORT", '3306')
DATABASE_NAME = os.environ.get("DATABASE_NAME", 'u6')
DATABASE_NAME_TEST = os.environ.get("DATABASE_NAME_TEST", 'u6_test')
DATABASE_NAME_PROD = os.environ.get("DATABASE_NAME_PROD", 'u6_prod')

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

# Get environment, or set to development by default
app_env = current_app.config.get('ENV', 'development')

# Settings applied to specific environments
if app_env == 'production':
    DATABASE_URI = 'mysql+pymysql://' \
        + DATABASE_USER+':' \
        + DATABASE_PASSWORD+'@' \
        + DATABASE_HOST+'/' \
        + DATABASE_NAME_PROD
elif app_env == 'development':
    DATABASE_URI = 'mysql+pymysql://' \
        + DATABASE_USER+':' \
        + DATABASE_PASSWORD+'@' \
        + DATABASE_HOST+'/' \
        + DATABASE_NAME
elif app_env == 'testing':
    DATABASE_URI = 'mysql+pymysql://' \
        + DATABASE_USER+':' \
        + DATABASE_PASSWORD+'@' \
        + DATABASE_HOST+'/' \
        + DATABASE_NAME_TEST
else:
    DATABASE_URI = 'mysql+pymysql://' \
        + DATABASE_USER+':' \
        + DATABASE_PASSWORD+'@' \
        + DATABASE_HOST+'/' \
        + DATABASE_NAME
# PyMySQL
engine = create_engine(DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    '''
    import all modules here that might define models so that
    they will be registered properly on the metadata.  Otherwise
    you will have to import them first before calling init_db()
    import models
    '''
    Base.metadata.create_all(bind=engine)


def drop_db():
    '''
    Drpp all tables for testing purpose!
    '''
    Base.metadata.drop_all(bind=engine)
