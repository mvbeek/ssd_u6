from tests.base import ReportTest
from tests.utils import (get_api,
                         post_api,
                         put_api_with_form,
                         delete_api,
                         json_format)


class TestUpload(ReportTest):
    def test_upload_succssfully(self):
        res = put_api_with_form(
            self, '/api/v1/report/upload', data=self.upload_data)
        self.assertEqual(res['meta']['code'], 200)
        self.assertEqual(res['response']['message'], 'Upload successful.')
        self.assertEqual(res['response']['reportname'], 'test_report')
        self.assertEqual(res['response']['description'], 'test_report')

    def test_upload_without_name(self):
        data = {'file': self.file, 'description': "hogehoge"}
        res = put_api_with_form(self, '/api/v1/report/upload', data=data)
        self.assertEqual(res['meta']['code'], 422)
        self.assertEqual(res['response']['error'], 'Invalid input.')

    def test_upload_with_traversal_attack(self):
        data = {'name': self.path_traversal,
                'file': self.file,
                'description': self.path_traversal}
        res = put_api_with_form(self, '/api/v1/report/upload', data=data)
        self.assertEqual(res['meta']['code'], 200)
        self.assertEqual(res['response']['message'], 'Upload successful.')
        self.assertEqual(res['response']['reportname'], 'etc_passwd')
        self.assertEqual(res['response']['description'], 'etc_passwd')

    def tesst_upload_with_directory_traversal_file_name(self):
        res = put_api_with_form(
            self, '/api/v1/report/upload', data=self.traversal_upload_data)
        self.assertEqual(res['meta']['code'], 422)
        self.assertEqual(res['response']['message'], 'Invalid file')

    def test_upload_directory_traversal_file_name_with_extension(self):
        res = put_api_with_form(
            self, '/api/v1/report/upload',
            data=self.traversal_upload_data_with_ext)
        self.assertEqual(res['meta']['code'], 200)
        self.assertEqual(res['response']['message'], 'Upload successful.')
        self.assertEqual(res['response']['filename'], 'etc_passwd.txt')
        self.assertEqual(res['response']['reportname'], 'etc_passwd')
        self.assertEqual(res['response']['description'], 'etc_passwd')

    def test_upload_with_external_source_input_to_file(self):
        data = {'name': self.path_traversal,
                'file': 'http://www.owasp.org/malicioustxt',
                'description': self.path_traversal}
        res = put_api_with_form(self, '/api/v1/report/upload', data=data)
        self.assertEqual(res['meta']['code'], 422)
        self.assertEqual(res['response']['error'], 'Invalid input.')


class TestRead(ReportTest):
    def test_read_report_not_exist(self):
        res = get_api(
            self, '/api/v1/report/read/150', token=self.regisered_auth_token)
        self.assertEqual(res['meta']['code'], 404)
        self.assertEqual(
            res['response']['error'], 'Report not found or invalid.')

    def test_read_report_successfully(self):
        put_api_with_form(self, '/api/v1/report/upload', data=self.upload_data)
        res = get_api(
            self, '/api/v1/report/read/1', token=self.regisered_auth_token)
        self.assertEqual(res['meta']['code'], 200)
        self.assertEqual(res['response']['name'], 'test_report')
        self.assertEqual(res['response']['description'], 'test_report')
        self.assertEqual(res['response']['file_name'], 'file.txt')

    def test_read_report_that_should_not_access_with_invalid_token(self):
        data = json_format(auth_token="invalidtoken")
        put_api_with_form(self, '/api/v1/report/upload', data=self.upload_data)
        delete_api(self, '/api/v1/auth/logout', token=self.auth_token_data)
        res = get_api(self, '/api/v1/report/read/1', token=data)
        self.assertEqual(res['meta']['code'], 401)
        self.assertRegexpMatches(
            res['response']['error'], 'You are not authenticate')

    def test_read_report_that_should_not_access(self):
        put_api_with_form(self, '/api/v1/report/upload', data=self.upload_data)
        data = json_format(
            email='valid@example.com', password='valid_password_example')
        post_api(self, '/api/v1/auth/register', data=data)
        token = post_api(
            self, '/api/v1/auth/login', data=data)['response']['auth_token']
        res = get_api(
            self, '/api/v1/report/read/1', token={'auth_token': token})
        self.assertEqual(res['meta']['code'], 404)
        self.assertEqual(
            res['response']['error'], 'Report not found or invalid.')
