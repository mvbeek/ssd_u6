'''
This is the main file of the flask app.
This will run the flask app.
'''
import sys
from flask import Flask


def create_app(test_config=None):
    '''
    This is the main function of the flask app.
    Depending on the environment, it will run the flask app with
    different configurations.
    '''
    # Disable Pylint import-outside-toplevel in this function.
    # pylint: disable=import-outside-toplevel
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    with app.app_context():
        app.config.from_object("api.conf.security.BaseConfig")

        if test_config is None or test_config == "prod":
            app.config.from_object("api.conf.security.ProductionConfig")
            app.config['ENV'] = "production"
        elif test_config == "dev":
            app.config.from_object("api.conf.security.DevelopmentConfig")
        elif test_config == "test":
            app.config.from_object("api.conf.security.TestingConfig")
            app.config['ENV'] = "testing"
        else:
            app.config.from_object("api.conf.security.DevelopmentConfig")
            app.config['ENV'] = "development"

    app.app_context().push()

    from api.conf.routes import generate_routes
    from flask_security import Security, SQLAlchemySessionUserDatastore
    from api.conf.database import db_session, init_db
    from api.models import User, Role

    generate_routes(app)

    # Setup Flask-Security
    user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
    Security(app, user_datastore)

    init_db()

    @app.after_request
    def add_header(response):
        '''
        As the OWASP ZAP detected X-Content-Type-Options header as a potential
        security vulnerability, we will add it to the response.
        Also, add different security practices that Flask recommends.
        '''
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Content-Security-Policy'] = ("default-src 'none';"
                                                       "script-src 'self';"
                                                       "connect-src 'self';"
                                                       "img-src 'self';"
                                                       "style-src 'self';"
                                                       "base-uri 'self';"
                                                       "form-action 'self'")
        return response
    return app


if __name__ == "__main__":
    if len(sys.argv) > 1:
        instance = create_app(sys.argv[1])
    else:
        instance = create_app()
    instance.run(port=5000)
