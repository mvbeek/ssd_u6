import json
from app import create_app
from unittest import TestCase


def json_format(**data):
    return json.dumps(dict(data))


def post_api(self, url, data=None):
    return self.app.post(url, data=data, content_type='application/json')


def format_response(response):
    return json.loads(response.get_data(as_text=True))


class TestRegister(TestCase):
    def setUp(self):
        self.app = create_app('test').test_client()
        from api.conf.database import drop_db, init_db, db_session
        db_session.commit()
        drop_db()
        init_db()
        self.weak_password = 'password'
        self.strong_password = 'dsafldakjhgdagfd21231gadsgas!DAFa'
        self.email = 'example@example.com'
        self.weak_data = json_format(email=self.email,
                                     password=self.weak_password)
        self.strong_data = json_format(email=self.email,
                                       password=self.strong_password)

    def test_register_with_weak_password(self):
        response = post_api(self, '/api/v1/auth/register', data=self.weak_data)
        data = format_response(response)
        self.assertEqual(data['meta']['code'], 403)
        self.assertEqual(data['response']['message'], 'A vulnerable password.')

    def test_register_with_strong_password(self):
        response = post_api(self, '/api/v1/auth/register',
                            data=self.strong_data)
        data = format_response(response)
        self.assertEqual(data['meta']['code'], 200)
        self.assertEqual(data['response']['message'], 'Register successful.')

    def test_register_with_email_none(self):
        data = json_format(email=None, password=self.strong_password)
        response = post_api(self, '/api/v1/auth/register', data=data)
        data = format_response(response)
        self.assertEqual(data['meta']['code'], 422)
        self.assertEqual(data['response']['message'], 'Invalid input.')

    def test_register_with_password_none(self):
        data = json_format(email=self.email, password=None)
        response = post_api(self, '/api/v1/auth/register', data=data)
        data = format_response(response)
        self.assertEqual(data['meta']['code'], 422)
        self.assertEqual(data['response']['message'], 'Invalid input.')

    def test_register_with_valid_credentials_and_irrelevant_attribute(self):
        data = json_format(email=self.email, password=self.strong_password,
                           irrelevant_attribute='irrelevant_attribute')
        response = post_api(self, '/api/v1/auth/register', data=data)
        data = format_response(response)
        self.assertEqual(data['meta']['code'], 200)
        self.assertEqual(data['response']['message'], 'Register successful.')

    def test_register_with_invalid_email(self):
        data = json_format(email='example@example',
                           password=self.strong_password)
        response = post_api(self, '/api/v1/auth/register', data=data)
        data = format_response(response)
        self.assertEqual(data['meta']['code'], 422)
        self.assertEqual(data['response']['message'], 'Invalid Email.')

    def test_register_with_duplicated_email(self):
        post_api(self, '/api/v1/auth/register', data=self.strong_data)
        response = post_api(self, '/api/v1/auth/register',
                            data=self.strong_data)
        data = format_response(response)
        self.assertEqual(data['meta']['code'], 409)
        self.assertEqual(data['response']['message'], 'Already exists.')
