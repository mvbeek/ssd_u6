'''
utility functions that support the following:
    1. formatting the response accordance with the flask-security convention.
    2. checking password strength.
For more detail, please see each function.
'''
from flask import jsonify
from flask_security import password_length_validator, \
                            password_complexity_validator, \
                            password_breached_validator, \
                            pwned


def render_json(payload, code):
    '''
    Render json as per flask-security convention.
    input:
        payload = json payload
        code = http status code
    '''
    response = jsonify(meta={'code': code}, response=payload)
    return response


def is_password_safe(email, password):
    '''
    Check if password is safe as per the follwing rules:
        1. Password length (password_length_validator)
        2. Password complexity (password_complexity_validator)
        3. Password breached (password_breached_validator)
        4. How many times password has been leaked (pwned)

    If any of the above rules are violated, return False.
    '''
    plv = password_length_validator(password=password) is None
    pcv = password_complexity_validator(password=password,
                                        is_register=True,
                                        email=email) is None
    pbv = password_breached_validator(password=password) is None
    pwn = pwned(password=password) == 0
    return plv and pcv and pbv and pwn
