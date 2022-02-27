import json


def json_format(**data):
    return json.dumps(dict(data))


def post_api(self, url, data=None):
    return self.app.post(url, data=data, content_type='application/json')


def format_response(response):
    return json.loads(response.get_data(as_text=True))
