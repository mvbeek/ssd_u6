from unittest import TestCase
from app import create_app
from tests.utils import json_format, post_api


class BaseTest(TestCase):

    def setUp(self):
        self.app = create_app('test').test_client()
        from api.conf.database import drop_db, init_db, db_session
        db_session.commit()
        drop_db()
        init_db()
        self.weak_password = 'password'
        self.strong_password = 'dsafldakjhgdagfd21231gadsgas!DAFa'
        self.leaked_password = 'mydarlingbob'
        self.wrong_password = 'wrongpassword'
        self.email = 'example@example.com'
        self.registered_user_email = 'registered@exmple.com'
        self.injection_password = 'password" or "1=1'
        self.injection_code = "' or 1=1--'"
        self.injection_email = 'example@example.com" or "1=1'
        self.path_traversal = '../../../'
        self.weak_data = json_format(email=self.email,
                                     password=self.weak_password)
        self.strong_data = json_format(email=self.email,
                                       password=self.strong_password)
        self.registered_user_data = json_format(
            email=self.registered_user_email,
            password=self.strong_password)
        post_api(self, '/api/v1/auth/register', data=self.registered_user_data)
        res = post_api(
            self, '/api/v1/auth/login', data=self.registered_user_data)
        self.regisered_auto_token = res['response']['auth_token']
