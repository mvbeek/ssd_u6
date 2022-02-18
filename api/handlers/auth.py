from flask import request
from flask_restful import Resource
from flask_security import verify_password, hash_password, \
                           SQLAlchemySessionUserDatastore, \
                           password_length_validator, \
                           password_complexity_validator, \
                           password_breached_validator, \
                           pwned, uia_email_mapper, \
                           auth_required
from flask_security.utils import find_user, login_user
from flask_security.core import UserMixin
from database import db_session, init_db
from models import User, Role

user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)


def is_password_safe(email, password):
    """
    Validate the password
    """
    # import pdb; pdb.set_trace()
    if password_length_validator(password=password) is None and \
       password_complexity_validator(password=password,
                                     is_register=True,
                                     email=email) is None and \
       password_breached_validator(password=password) is None and \
       pwned(password=password) == 0:
        return True
    else:
        return False


class Index(Resource):
    @staticmethod
    @auth_required('token', 'session')
    def get():
        pass
        return "Hello Flask Restful Example!"


class Login(Resource):
    @staticmethod
    def post():
        try:
            email, password = (
                request.json['email'].strip(),
                request.json['password'].strip(),
            )
        except Exception:
            return ({"message": "Invalid input."}, 422)

        if email is None or password is None:
            return ({"message": "Invalid input."}, 422)

        user = User.query.filter_by(email=email).first()
        check_credential = verify_password(password, user.password)

        if user is None or check_credential is False:
            return ({"message": "Invalid credentials."}, 401)
        elif check_credential is True:
            # import pdb; pdb.set_trace()
            login_user(user,
                       remember=True)
            token = UserMixin.get_auth_token(user)
            db_session.commit()
            return {"message": "Login successful.",
                    "email": user.email,
                    "IP": user.current_login_ip,
                    "login count": user.login_count,
                    "active": user.active,
                    "auth_token": token,
                    # "fs_uniquifier": user.fs_uniquifier,
                    }, 200


class Register(Resource):
    @staticmethod
    def post():
        try:
            email, password = (
                request.json.get("email").strip(),
                request.json.get("password").strip(),
            )
        except Exception:
            return ({"message": "Invalid input."}, 422)

        if email is None or password is None:
            return ({"message": "Invalid input."}, 422)
        if find_user(email) is not None:
            return ({"message": "Already exists."}, 409)
        if uia_email_mapper(email) is None:
            return ({"message": "Invalid Email."}, 422)
        if is_password_safe(email, password) is False:
            return ({"message": "A vulnerable password."}, 403)
        password = hash_password(password)
        init_db()
        user_datastore.create_user(email=email, password=password)
        db_session.commit()
        return ({"message": "Register successful."}, 200)
