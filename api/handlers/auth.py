import uuid
from flask import request
from flask_restful import Resource
from flask_security import verify_password, hash_password, \
                           SQLAlchemySessionUserDatastore, \
                           uia_email_mapper, \
                           auth_required
from flask_security.utils import find_user, login_user, current_user
from flask_security.core import UserMixin
from api.conf.database import db_session, init_db
from api.models import User, Role
from api.utils import render_json, is_password_safe

user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)


class Index(Resource):
    @staticmethod
    @auth_required('token', 'session')
    def get():
        payload = {
                   'message': 'Hello Flask Restful Example!',
                   'user': current_user.email
                   }

        return render_json(payload, 200)


class Login(Resource):
    @staticmethod
    def post():
        try:
            email, password = (
                request.json['email'].strip(),
                request.json['password'].strip(),
            )
        except Exception:
            return render_json({"error": "Invalid input."}, 422)

        if email is None or password is None:
            return render_json({"error": "Invalid input."}, 422)

        user = User.query.filter_by(email=email).first()
        if user is None:
            return render_json({"error": "Invalid credentials."}, 401)

        check_credential = verify_password(password, user.password)

        if check_credential is False:
            return render_json({"error": "Invalid credentials."}, 401)

        login_user(user,
                   remember=True)
        token = UserMixin.get_auth_token(user)
        db_session.commit()
        payload = {"message": "Login successful."
                   "Use this auth_token when you call APIs",
                   "auth_token": token,
                   }
        return render_json(payload, 200)


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
        return render_json({"message": "Register successful."}, 200)


class ChangePassword(Resource):
    @staticmethod
    @auth_required()
    def post():
        try:
            current_password, new_password = (
                request.json.get("current_password").strip(),
                request.json.get("new_password").strip())
        except Exception:
            return render_json({"message": "Invalid input."}, 422)

        if current_password is None or new_password is None:
            return render_json({"message": "Invalid input."}, 422)

        if verify_password(current_password, current_user.password) is False:
            return render_json({"message": "Invalid credentials."}, 401)

        if is_password_safe(current_user.email, new_password) is False:
            return ({"message": "A vulnerable password."}, 403)

        password = hash_password(new_password)
        user = User.query.filter_by(id=current_user.id).first()
        user.password = password
        user.fs_uniquifier = uuid.uuid4().hex
        db_session.commit()
        return render_json({"message": "Change password successful."
                            "You need to re-login to get new auth_token"}, 200)


class Logout(Resource):
    @staticmethod
    @auth_required('token', 'session')
    def get():
        user = User.query.filter_by(id=current_user.id).first()
        # this will immediately logout the user by deleting the token
        user.fs_uniquifier = uuid.uuid4().hex
        db_session.commit()
        return render_json({"message": "Logout successful."}, 200)


class DeleteUser(Resource):
    @staticmethod
    @auth_required('token', 'session')
    def get():
        user = current_user
        db_session.delete(user)
        db_session.commit()
        return render_json({"message": "User deleted."}, 200)
