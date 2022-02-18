from flask_restful import Api
from api.handlers.auth import (Index, Login, Register)
from api.handlers.report import (List)


def generate_routes(app):
    api = Api(app)

    # auth microservice
    api.add_resource(Index, '/api/v1/auth/index')
    api.add_resource(Login, '/api/v1/auth/login')
    api.add_resource(Register, '/api/v1/auth/register')

    # report microservice
    api.add_resource(List, '/api/v1/report/list')
