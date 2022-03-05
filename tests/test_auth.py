'''
This file takes care of testing scripts of the auth API.
'''

from .base import BaseTest, LoginTest
from .utils import json_format, post_api, get_api


class TestRegister(BaseTest):
    '''
    This class represents auth/register API test cases.
    '''
    def test_register_with_weak_password(self):
        '''
        This test case is to test the user registration case
        "when the password is weak."
        '''
        res = post_api(self, '/api/v1/auth/register', data=self.weak_data)
        self.assertEqual(res['meta']['code'], 403)
        self.assertEqual(res['response']['error'], 'A vulnerable password.')

    def test_register_with_strong_password(self):
        '''
        This test case is to test the user registration case
        "when the password is strong."
        '''
        res = post_api(self, '/api/v1/auth/register', data=self.strong_data)
        self.assertEqual(res['meta']['code'], 200)
        self.assertEqual(res['response']['message'], 'Register successful.')

    def test_register_with_email_none(self):
        '''
        This test case is to test the user registration case
        "when the email is None."
        '''
        data = json_format(email=None, password=self.strong_password)
        res = post_api(self, '/api/v1/auth/register', data=data)
        self.assertEqual(res['meta']['code'], 422)
        self.assertEqual(res['response']['error'], 'Invalid input.')

    def test_register_with_password_none(self):
        '''
        This test case is to test the user registration case
        "when the password is None."
        '''
        data = json_format(email=self.email, password=None)
        res = post_api(self, '/api/v1/auth/register', data=data)
        self.assertEqual(res['meta']['code'], 422)
        self.assertEqual(res['response']['error'], 'Invalid input.')

    def test_register_with_valid_credentials_and_irrelevant_attribute(self):
        '''
        This test case is to test the user registration case
        "when posting valid credentials with irrelevant attributes."
        '''
        data = json_format(email=self.email, password=self.strong_password,
                           irrelevant_attribute='irrelevant_attribute')
        res = post_api(self, '/api/v1/auth/register', data=data)
        self.assertEqual(res['meta']['code'], 200)
        self.assertEqual(res['response']['message'], 'Register successful.')

    def test_register_with_invalid_email(self):
        '''
        This test case is to test the user registration case
        "when the email is invalid."
        '''
        data = json_format(email='example@example',
                           password=self.strong_password)
        res = post_api(self, '/api/v1/auth/register', data=data)
        self.assertEqual(res['meta']['code'], 422)
        self.assertEqual(res['response']['error'], 'Invalid Email.')

    def test_register_with_duplicated_email(self):
        '''
        This test case is to test the user registration case
        "when the email is duplicated."
        '''
        post_api(self, '/api/v1/auth/register', data=self.strong_data)
        res = post_api(self, '/api/v1/auth/register', data=self.strong_data)
        self.assertEqual(res['meta']['code'], 409)
        self.assertEqual(res['response']['error'], 'Already exists.')

    def test_register_with_leaked_password(self):
        '''
        This test case is to test the user registration case
        "when the password is leaked."
        '''
        data = json_format(email=self.email, password=self.leaked_password)
        res = post_api(self, '/api/v1/auth/register', data=data)
        self.assertEqual(res['meta']['code'], 403)
        self.assertEqual(res['response']['error'], 'A vulnerable password.')

    def test_register_if_password_is_the_same_as_email(self):
        '''
        This test case is to test the user registration case
        "when the password is the same as email."
        '''
        data = json_format(email=self.email, password=self.email)
        res = post_api(self, '/api/v1/auth/register', data=data)
        self.assertEqual(res['meta']['code'], 403)
        self.assertEqual(res['response']['error'], 'A vulnerable password.')


class TestLogin(LoginTest):
    '''
    This class represents auth/login API test cases.
    '''
    def test_login_with_user_does_not_exist(self):
        '''
        This test case is to test the user login case
        "when the user does not exist."
        '''
        res = post_api(self, '/api/v1/auth/login', data=self.weak_data)
        self.assertEqual(res['meta']['code'], 401)
        self.assertEqual(res['response']['error'], 'Invalid credentials.')

    def test_login_with_valid_credentials(self):
        '''
        This test case is to test the user login case
        "when the email and password are valid."
        '''
        res = post_api(self, '/api/v1/auth/login',
                       data=self.registered_user_data)
        self.assertEqual(res['meta']['code'], 200)
        self.assertRegex(
            res['response']['message'], 'Login successful.')

    def test_login_with_wrong_password(self):
        '''
        This test case is to test the user login case
        "when the password is wrong."
        '''
        data = json_format(email=self.email, password='wrong_password')
        res = post_api(self, '/api/v1/auth/login', data=data)
        self.assertEqual(res['meta']['code'], 401)
        self.assertEqual(res['response']['error'], 'Invalid credentials.')
        data = json_format(email=self.registered_user_email,
                           password=self.wrong_password)
        res = post_api(self, '/api/v1/auth/login', data=data)
        self.assertEqual(res['meta']['code'], 401)
        self.assertEqual(res['response']['error'], 'Invalid credentials.')

    def test_login_with_irrelevant_attribute(self):
        '''
        This test case is to test the user login case
        "when the valid email and password
        with irrelevant attributes are posted."
        '''
        data = json_format(
            email=self.registered_user_email,
            password=self.strong_password,
            irrelevant_attribute='irrelevant_attribute')
        res = post_api(self, '/api/v1/auth/login', data=data)
        self.assertEqual(res['meta']['code'], 200)
        self.assertRegex(
            res['response']['message'], 'Login successful.')

    def test_login_with_injection_email(self):
        '''
        This test case is to test the user login case
        "when the email parameter is injection code"
        '''
        data = json_format(email=self.injection_email,
                           password=self.strong_password)
        res = post_api(self, '/api/v1/auth/login', data=data)
        self.assertEqual(res['meta']['code'], 401)
        self.assertEqual(res['response']['error'], 'Invalid credentials.')

    def test_login_with_injection_code_in_email(self):
        '''
        This test case is to test the user login case
        "when the email parameter is injection code"
        '''
        data = json_format(email=self.injection_code,
                           password=self.strong_password)
        res = post_api(self, '/api/v1/auth/login', data=data)
        self.assertEqual(res['meta']['code'], 401)
        self.assertEqual(res['response']['error'], 'Invalid credentials.')

    def test_login_with_injection_password(self):
        '''
        This test case is to test the user login case
        "when the password parameter is injection code"
        '''
        data = json_format(email=self.registered_user_email,
                           password=self.injection_password)
        res = post_api(self, '/api/v1/auth/login', data=data)
        self.assertEqual(res['meta']['code'], 401)
        self.assertEqual(res['response']['error'], 'Invalid credentials.')

    def test_login_with_injection_code(self):
        '''
        This test case is to test the user login case
        "when the irrelevant parameter with injection code"
        '''
        data = json_format(email=self.registered_user_email,
                           code=self.injection_code)
        res = post_api(self, '/api/v1/auth/login', data=data)
        self.assertEqual(res['meta']['code'], 422)
        self.assertEqual(res['response']['error'], 'Invalid input')

    def test_login_with_path_traversal_attack(self):
        '''
        This test case is to test the user login case
        "when the email parameter is path traversal attack code"
        '''
        data = json_format(email=self.path_traversal,
                           password=self.path_traversal)
        res = post_api(self, '/api/v1/auth/login', data=data)
        self.assertEqual(res['meta']['code'], 401)
        self.assertEqual(res['response']['error'], 'Invalid credentials.')

    def test_login_with_os_command_injenction_attack(self):
        '''
        This test case is to test the user login case
        "when the email parameter is os command injenction attack code"
        '''
        data = json_format(email="foo-bar@example.com';start-sleep -s 15")
        res = post_api(self, '/api/v1/auth/login', data=data)
        self.assertEqual(res['meta']['code'], 422)
        self.assertEqual(res['response']['error'], 'Invalid input')


class TestIndex(LoginTest):
    '''
    This class represents auth/index API test cases.
    '''
    def test_index_with_valid_auth_token(self):
        '''
        This test case is to test the auth/index case
        "when the valid auth token is posted."
        '''
        res = get_api(self, '/api/v1/auth/index', token=self.auth_token_data)
        self.assertEqual(res['meta']['code'], 200)
        self.assertEqual(
            res['response']['message'], 'Hello Flask Restful Example!')
        self.assertEqual(res['response']['user'], self.registered_user_email)

    def test_index_with_invalid_auth_token(self):
        '''
        This test case is to test the auth/index case
        "when the invalid auth token is posted."
        '''
        data = json_format(auth_token="invalidtoken")
        res = get_api(self, '/api/v1/auth/index', token=data)
        self.assertEqual(res['meta']['code'], 401)
        self.assertRegex(
            res['response']['error'], 'You are not authenticated.')

    def test_index_without_auth_token(self):
        '''
        This test case is to test the auth/index case
        "when the auth token is not posted."
        '''
        res = get_api(self, '/api/v1/auth/index')
        self.assertEqual(res['meta']['code'], 401)
        self.assertRegex(
            res['response']['error'], 'You are not authenticated.')
