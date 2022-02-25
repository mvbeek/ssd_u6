'''
This is the main file of the flask app.
This will run the flask app.
'''
from flask import Flask
from flask_security import Security, SQLAlchemySessionUserDatastore
from api.conf.database import db_session, init_db
from api.models import User, Role
from api.conf.routes import generate_routes

app = Flask(__name__)
# app.config.from_object('api.conf.security.BaseConfig')
app.config.from_object('api.conf.security.DevelopmentConfig')

generate_routes(app)

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)

init_db()

if __name__ == '__main__':
    app.run()
