'''
This file takes care of security settings.
'''
import os

VALUE_ERROR_MSG = "No {} set for the Env Variable. Go to README for more info."


class BaseConfig():
    '''
    BaseConfig class that contains the base configuration.
    Applied to all evironments.
    '''
    DEBUG = False
    TESTING = False

    # the most recommended password hash algorithm by OWASP
    SECURITY_PASSWORD_HASH = 'argon2'  # nosec

    # Security Key
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError(VALUE_ERROR_MSG.format("SECRET_KEY"))

    # Password Salt
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
    if not SECURITY_PASSWORD_SALT:
        raise ValueError(VALUE_ERROR_MSG.format("SECURITY_PASSWORD_SALT"))

    # User registration function is activated.
    SECURITY_REGISTERABLE = True
    # Send registration email function is deactivated.
    SECURITY_SEND_REGISTER_EMAIL = False
    # If we implement TOTP. TBD
    SECURITY_TOTP_ISSUER = 'SSD Flask Security TOTP'

    # Password Validation Enhancement Configuration
    SECURITY_PASSWORD_COMPLEXITY_CHECKER = 'zxcvbn'  # nosec
    # prevent the breached password to register.
    SECURITY_PASSWORD_CHECK_BREACHED = True
    '''
    Unicode passwords should be normalized as specified
    by NIST requirement: 5.1.1.2
    Ref: https://pages.nist.gov/800-63-3/sp800-63b.html#sec5
    '''
    SECURITY_PASSWORD_NORMALIZE_FORM = 'NFKD'  # nosec

    # Store User Tracking Data such as IP, last login time, etc.
    SECURITY_TRACKABLE = True
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = False


class DevelopmentConfig(BaseConfig):
    '''
    DevelopmentConfig class that contains
    the development environment configuration.
    '''
    DEBUG = True
    TESTING = True
    FLASK_ENV = 'development'


class TestingConfig(BaseConfig):
    '''
    TestingConfig class that contains
    the testing environment configuration.
    '''
    DEBUG = False
    TESTING = True


class ProductionConfig(BaseConfig):
    '''
    ProductionConfig class that contains
    the production environment configuration.
    '''
    DEBUG = False
    TESTING = False
