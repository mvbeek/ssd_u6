import json


def json_format(**data):
    return json.dumps(dict(data))


def format_response(response):
    return json.loads(response.get_data(as_text=True))


def post_api(self, url, data=None):
    response = self.app.post(url, data=data, content_type='application/json')
    return json.loads(response.get_data(as_text=True))


def get_api(self, url, token=None):
    response = self.app.get(
        url,
        data=token,
        content_type='application/json')
    return json.loads(response.get_data(as_text=True))


def delete_api(self, url, token=None):
    response = self.app.delete(
        url,
        data=token,
        content_type='application/json')
    return json.loads(response.get_data(as_text=True))


def put_api_with_form(self, url, data=None):
    response = self.app.put(url, data=data, content_type='multipart/form-data')
    return json.loads(response.get_data(as_text=True))
