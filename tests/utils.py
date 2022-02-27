import json


def json_format(**data):
    return json.dumps(dict(data))


def format_response(response):
    return json.loads(response.get_data(as_text=True))


def post_api(self, url, data=None):
    response = self.app.post(url, data=data, content_type='application/json')
    return json.loads(response.get_data(as_text=True))
