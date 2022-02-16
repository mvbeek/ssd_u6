from flask import Flask, render_template_string, jsonify, request
from flask_security import Security, current_user, auth_required, hash_password, \
     SQLAlchemySessionUserDatastore, login_required, login_user, logout_user, verify_password
from database import db_session, init_db
from models import User, Role
from api.conf.routes import generate_routes

app = Flask(__name__)
# app.config.from_object('config.BaseConfig')
app.config.from_object('config.DevelopmentConfig')

generate_routes(app)

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
    init_db()


# Views
@app.route("/")
@auth_required()
def home():
    return render_template_string('Hello {{email}} !', email=current_user.email)


if __name__ == '__main__':
    app.run()
