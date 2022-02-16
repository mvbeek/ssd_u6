from flask import g, request
from flask_restful import Resource
from flask_security import verify_password, login_user

from models import User, Role

class Login(Resource):
    @staticmethod
    def post():
        try:
            email, password = (
                request.json['email'].strip(),
                request.json['password'].strip(),
            )
        except Exception as why:
            return ({"message": "Invalid input."}, 422)

        if email is None or password is None:
            return ({"message": "Invalid input."}, 422)
        
        user = User.query.filter_by(email=email).first()
        check_credential = verify_password(password, user.password)
        print(check_credential)

        if user is None or check_credential is False:
            return ({"message": "Invalid credentials."}, 401)
        elif check_credential is True:
            login_user(user)
            return ({"message": "Login successful."}, 200)
