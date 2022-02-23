'''
This file represents the auth microservice.
Auth microservice is responsible for user authentication such as
register user, login, logout, change password, and delete user.
'''
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
    '''
    This class represents the index of the auth microservice.
    Mainly used for testing purposes.
    auth_token is necessary.

    method: GET
    url: /api/v1/auth/index

    example httpie request:
        http GET http://127.0.0.1:5000/api/v1/auth/index \
            auth_token=GET_AUTH_TOKEN_WITH_LOGIN_API_AND_PASTE_HERE

    response:
        {
            "meta": {
                "code": 200
            },
            "response": {
                "message": "Hello Flask Restful Example!",
                "user": "example@example.com"
            }
        }
    '''

    # decorators: auth_token is necessary
    @staticmethod
    @auth_required('token')
    def get():
        '''
        This method is used for testing purposes.
        Simply returns a message and the current user's email
        in JSON format.
        '''
        payload = {
                   'message': 'Hello Flask Restful Example!',
                   'user': current_user.email
                   }

        return render_json(payload, 200)


class Login(Resource):
    '''
    This class represents the login of the auth microservice.
    Login is necessary to generate auth_token.

    method: POST
    url: /api/v1/auth/login
    required input parameters:
        email: user email
        password: user password

    example httpie request:
        http POST http://127.0.0.1:5000/api/v1/auth/login \
            email='example@example.com' password='example_password'

    response:
        {
            "meta": {
                "code": 200
            },
            "response": {
                "auth_token": "xxxxxxx.xxxxxx.xxxxx",
                "message": "Login successful.Use this auth_token when you call APIs"
            }
        }

    '''
    @staticmethod
    def post():
        '''
        This method is used for user login.
        '''
        email, password = (
            request.json['email'].strip(),
            request.json['password'].strip(),
            )

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
    '''
    This class represents the register of the auth microservice.

    method: POST
    url: /api/v1/auth/register
    required input parameters:
        email: user email
        password: user password

    example httpie request:
        http POST http://127.0.0.1:5000/api/v1/auth/register \
            email=example@example.com password=example_password

    response:
        {
            "meta": {
                "code": 200
            },
            "response": {
                "message": "Register successful."
            }
        }
    '''
    @staticmethod
    def post():
        '''
        This method is used for user registration.
        '''
        email, password = (
            request.json.get("email").strip(),
            request.json.get("password").strip(),
            )

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
    '''
    This class represents the change password of the auth microservice.
    auth_token is necessary.

    method: PUT
    url: /api/v1/auth/change_password
    required input parameters:
        current_password: user old password
        new_password: user new password

    example httpie request:
        http PUT http://127.0.0.1:5000/api/v1/auth/change_password \
            current_password=example_password new_password=example_password

    response:
        {
            "meta": {
                "code": 200
            },
            "response": {
                "message": "Change password successful.
                            You need to re-login to get new auth_token"
            }
        }
    '''
    @staticmethod
    @auth_required()
    def put():
        '''
        This method is used for user password change.
        '''
        current_password, new_password = (
            request.json.get("current_password").strip(),
            request.json.get("new_password").strip()
            )

        if current_password is None or new_password is None:
            return render_json({"message": "Invalid input."}, 422)

        if verify_password(current_password, current_user.password) is False:
            return render_json({"message": "Invalid credentials."}, 401)

        if is_password_safe(current_user.email, new_password) is False:
            return ({"message": "A vulnerable password."}, 403)

        password = hash_password(new_password)
        user = User.query.filter_by(id=current_user.id).first()
        user.password = password
        # this will immediately logout the user by deleting the token
        user.fs_uniquifier = uuid.uuid4().hex
        db_session.commit()
        return render_json({"message": "Change password successful."
                            "You need to re-login to get new auth_token"}, 200)


class Logout(Resource):
    '''
    This class represents the logout of the auth microservice.
    auth_token is necessary.

    method: DELETE
    url: /api/v1/auth/logout

    example httpie request:
            http GET http://127.0.0.1:5000/api/v1/auth/logout \
                auth_token=xxxxxxx.xxxxxx.xxxxx
    '''
    @staticmethod
    @auth_required('token')
    def delete():
        '''
        This method is used for user logout.
        '''
        user = User.query.filter_by(id=current_user.id).first()
        # this will immediately logout the user by deleting the token
        user.fs_uniquifier = uuid.uuid4().hex
        db_session.commit()
        return render_json({"message": "Logout successful."}, 200)


class DeleteUser(Resource):
    '''
    This class represents the delete user of the auth microservice.
    auth_token is necessary.

    method: DELETE
    url: /api/v1/auth/delete_user

    example httpie request:
        http DELETE http://127.0.0.1:5000/api/v1/auth/delete_user \
            auth_token=xxxxxxx.xxxxxx.xxxxx
    '''
    @staticmethod
    @auth_required('token')
    def delete():
        '''
        This method is used for user deletion.
        '''
        user = current_user
        db_session.delete(user)
        db_session.commit()
        return render_json({"message": "User deleted."}, 200)
