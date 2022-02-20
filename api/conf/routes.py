from flask_restful import Api
from api.handlers.auth import (Index, Login, Register)
from api.handlers.report import (List, Upload, Read, Download)


def generate_routes(app):
    api = Api(app)

    # auth microservice
    api.add_resource(Index, '/api/v1/auth/index')
    api.add_resource(Login, '/api/v1/auth/login')
    api.add_resource(Register, '/api/v1/auth/register')

    # report microservice
    api.add_resource(List, '/api/v1/report/list')
    api.add_resource(Upload, '/api/v1/report/upload')
    api.add_resource(Read, '/api/v1/report/read/<int:id>')
    api.add_resource(Download, '/api/v1/report/download/<int:id>')
