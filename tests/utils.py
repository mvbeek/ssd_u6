'''
This file takes care of utility scripts for testing.
'''


import json


def json_format(**data):
    '''
    This function is to format the data in json format.
    '''
    return json.dumps(dict(data))


def format_response(response):
    '''
    This function is to format the response into json format.
    '''
    return json.loads(response.get_data(as_text=True))


def post_api(self, url, data=None):
    '''
    This function is to post data to the API and
    return the json response.
    '''
    response = self.app.post(url, data=data, content_type='application/json')
    return format_response(response)


def get_api(self, url, token=None):
    '''
    This function is to send GET to the API and
    return the json response.
    '''
    response = self.app.get(
        url,
        data=token,
        content_type='application/json')
    return format_response(response)


def delete_api(self, url, token=None):
    '''
    This function is to send DELETE to the API and
    return the json response.
    '''
    response = self.app.delete(
        url,
        data=token,
        content_type='application/json')
    return format_response(response)


def post_api_with_form(self, url, data=None):
    '''
    This function is to post form data to the API and
    return the json response.
    '''
    response = self.app.post(
        url,
        data=data,
        content_type='multipart/form-data')
    return format_response(response)
