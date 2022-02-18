from flask_restful import Resource
from flask_security import auth_required


class List(Resource):
    @staticmethod
    @auth_required()
    def get():
        return "Hello Flask Restful Example!"
