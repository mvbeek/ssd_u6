'''
This file takes care of routes.
'''
from flask_restful import Api
from api.handlers.auth import (Index,
                               Login,
                               Register,
                               ChangePassword,
                               Logout,
                               DeleteUser)
from api.handlers.report import (List,
                                 Upload,
                                 Read,
                                 Download)


def generate_routes(app):
    '''
    Generate routes for the API.
    Supports multiple versions for the future scalability.
    Two microservices are supported, auth and report.
    '''
    api = Api(app)

    # auth microservice
    api.add_resource(Index, '/api/v1/auth/index')
    api.add_resource(Login, '/api/v1/auth/login')
    api.add_resource(Register, '/api/v1/auth/register')
    api.add_resource(ChangePassword, '/api/v1/auth/change_password')
    api.add_resource(Logout, '/api/v1/auth/logout')
    api.add_resource(DeleteUser, '/api/v1/auth/delete_user')

    # report microservice
    api.add_resource(List, '/api/v1/report/list')
    api.add_resource(Upload, '/api/v1/report/upload')
    api.add_resource(Read, '/api/v1/report/read/<int:report_id>')
    api.add_resource(Download, '/api/v1/report/download/<int:report_id>')
