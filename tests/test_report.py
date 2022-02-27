from tests.base import ReportTest
from tests.utils import put_api_with_form


class TestUpload(ReportTest):
    def test_upload_succssfully(self):
        res = put_api_with_form(
            self, '/api/v1/report/upload', data=self.upload_data)
        print(res)
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
        print(res)
        self.assertEqual(res['meta']['code'], 200)
        self.assertEqual(res['response']['message'], 'Upload successful.')
        self.assertEqual(res['response']['reportname'], 'etc_passwd')
        self.assertEqual(res['response']['description'], 'etc_passwd')

    def tesst_upload_with_directory_traversal_file_name(self):
        res = put_api_with_form(
            self, '/api/v1/report/upload', data=self.traversal_upload_data)
        print(res)
        self.assertEqual(res['meta']['code'], 422)
        self.assertEqual(res['response']['message'], 'Invalid file')

    def test_upload_directory_traversal_file_name_with_extension(self):
        res = put_api_with_form(
            self, '/api/v1/report/upload',
            data=self.traversal_upload_data_with_ext)
        print(res)
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
        print(res)
        self.assertEqual(res['meta']['code'], 422)
        self.assertEqual(res['response']['error'], 'Invalid input.')
