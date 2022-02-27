import io
import base64
from unittest import TestCase
from app import create_app
from tests.utils import json_format, post_api
from werkzeug.datastructures import FileStorage


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
        self.path_traversal = '../../../'
        self.weak_data = json_format(email=self.email,
                                     password=self.weak_password)
        self.strong_data = json_format(email=self.email,
                                       password=self.strong_password)


class LoginTest(TestCase):

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
        self.regisered_auth_token = res['response']['auth_token']
        self.auth_token_data = json_format(
            auth_token=self.regisered_auth_token)


class ReportTest(TestCase):

    def setUp(self):
        self.app = create_app('test').test_client()
        from api.conf.database import drop_db, init_db, db_session
        db_session.commit()
        drop_db()
        init_db()
        self.registered_user_email = 'registered@exmple.com'
        self.strong_password = 'dsafldakjhgdagfd21231gadsgas!DAFa'
        self.registered_user_data = json_format(
            email=self.registered_user_email,
            password=self.strong_password)
        post_api(self, '/api/v1/auth/register', data=self.registered_user_data)
        res = post_api(
            self, '/api/v1/auth/login', data=self.registered_user_data)
        self.regisered_auth_token = res['response']['auth_token']
        self.auth_token_data = json_format(
            auth_token=self.regisered_auth_token)
        self.blob_data = io.BytesIO(base64.b64decode(b'file contents'))
        self.file = FileStorage(
            stream=self.blob_data,
            filename='file.txt',
            content_type='text/plain')
        self.upload_data = {
            'auth_token': self.regisered_auth_token,
            'file': self.file,
            'name': 'test_report',
            'description': 'test report'}
        self.path_traversal = '../../../etc/passwd'
        self.traversal_blob_data = io.BytesIO(b'../../../etc/passwd')
        self.traversal_file = FileStorage(
            stream=self.traversal_blob_data,
            filename=self.path_traversal)
        self.traversal_file_with_ext = FileStorage(
            stream=self.traversal_blob_data,
            filename=self.path_traversal + '.txt')
        self.traversal_upload_data = {
            'auth_token': self.regisered_auth_token,
            'file': self.traversal_file,
            'name': self.path_traversal,
            'description': self.path_traversal}
        self.traversal_upload_data_with_ext = {
            'auth_token': self.regisered_auth_token,
            'file': self.traversal_file_with_ext,
            'name': self.path_traversal,
            'description': self.path_traversal}
