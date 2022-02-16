from flask_restful import Api

from api.handlers.auth import (Login)

def generate_routes(app):
    api = Api(app)
    api.add_resource(Login, '/api/v1/auth/login')