import os

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for Flask application")
SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
if not SECURITY_PASSWORD_SALT:
    raise ValueError("No SECURITY_PASSWORD_SALT set for Flask application")


class BaseConfig():
    DEBUG = False
    TESTING = False

    # the most recommended password hash algorithm by OWASP
    SECURITY_PASSWORD_HASH = 'argon2'  # nosec
    SECRET_KEY = SECRET_KEY
    SECURITY_PASSWORD_SALT = SECURITY_PASSWORD_SALT
    SECURITY_PASSWORD_COMPLEXITY_CHECKER = 'zxcvbn'  # nosec
    # prevent the breached password to register.
    SECURITY_PASSWORD_CHECK_BREACHED = True
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = False
    SECURITY_TOTP_ISSUER = 'SSD Flask Security TOTP'
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    '''
    Unicode passwords should be normalized as specified
    by NIST requirement: 5.1.1.2
    Ref: https://pages.nist.gov/800-63-3/sp800-63b.html#sec5
    '''
    SECURITY_PASSWORD_NORMALIZE_FORM = 'NFKD'  # nosec


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    FLASK_ENV = 'development'


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
