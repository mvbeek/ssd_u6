from flask import jsonify
from flask_security import password_length_validator, \
                            password_complexity_validator, \
                            password_breached_validator, \
                            pwned


def render_json(payload, code):
    """
    Render json as per flask-security convention.
    """
    response = jsonify(meta={'code': code}, response=payload)
    return response


def is_password_safe(email, password):
    """
    Check if password is safe.
    1. Password length (password_length_validator)
    2. Password complexity (password_complexity_validator)
    3. Password breached (password_breached_validator)
    4. How many times password has been leaked (pwned)
    """
    # import pdb; pdb.set_trace()
    if password_length_validator(password=password) is None and \
        password_complexity_validator(password=password,
                                      is_register=True,
                                      email=email) is None and \
        password_breached_validator(password=password) is None and \
            pwned(password=password) == 0:
        return True
    else:
        return False