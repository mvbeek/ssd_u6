'''
This file represents the report microservice.
Report microservice is responsible for report management, including
    - Listing all reports
    - Uploading a report
    - Reading a report
    - Downloading a report
'''
import os
from pathlib import Path
from flask import request, send_from_directory
from werkzeug.utils import secure_filename
from flask_restful import Resource
from flask_security import auth_required, current_user, \
                           SQLAlchemySessionUserDatastore
from api.utils import render_json
from api.models import Report, User, ReportSchema
from api.conf.database import db_session

# Upload Folder
UPLOAD_FOLDER = os.path.abspath(
                    os.path.join(
                        Path(__file__).parent.parent.parent,
                        'static',
                        'uploads'))
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
report_datastore = SQLAlchemySessionUserDatastore(db_session, Report, User)


def allowed_file(filename):
    '''
    Restricts file types to be uploaded.
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class List(Resource):
    '''
    This class represents the list of all reports of logged in user.
    auth_token is necessary.

    method: GET
    url: /api/v1/report/list

    example httpie request:
        http GET http://127.0.0.1:5000/api/v1/report/list \
             Authentication-Token:GET_AUTH_TOKEN_WITH_LOGIN_API_AND_PASTE_HERE

    response:
        {
            "meta": {
                "code": 200
            },
            "response": [
                {
                    "created_at": "2022-02-23T02:10:56",
                    "description": "This is description",
                    "file_name": "example.pdf",
                    "id": 1,
                    "name": "This is report name",
                    "updated_at": "2022-02-23T02:10:56",
                    "url": "/path/to/file/example.pdf",
                    "user": 1
                }
            ]
        }
    '''
    @staticmethod
    @auth_required()
    def get():
        '''
        This method is used for listing all reports of logged in user.
        '''
        # Get the user's reports
        reports = Report.query.filter_by(user_id=current_user.id).all()
        # Serialize the reports
        report_schema = ReportSchema(many=True)
        payload = report_schema.dump(reports)
        return render_json(payload, 200)


class Upload(Resource):
    '''
    This class represents the upload of a report.
    auth_token is necessary.

    method: POST
    url: /api/v1/report/upload
    required input parameters:
        name: report name
        description: report description
        file: report file

    example httpie request:
        http POST http://127.0.0.1:5000/api/v1/report/upload \
            Authentication-Token:GET_AUTH_TOKEN_WITH_LOGIN_API_AND_PASTE_HERE \
            name='This is report name' \
            description='This is report description' \
            file@./example.pdf'

    response:
        {
            "meta": {
                "code": 200
            },
            "response": {
                "message": "Report uploaded successfully",
                "filename": "example.pdf",
                "reportname": "This is report name",
                "user": example@example.com
            }
        }
    '''
    @staticmethod
    @auth_required()
    def post():
        '''
        This method is used for uploading a report.
        '''
        try:
            name, description, file = (
                    request.form['name'].strip(),
                    request.form['description'].strip(),
                    request.files['file'],
            )
        except (KeyError, ValueError, AttributeError):
            return render_json({'error': 'Invalid input.'}, 422)
        if name is None or description is None or file is None:
            return render_json({"error": "Invalid input."}, 422)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            name = secure_filename(name)
            description = secure_filename(description)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            report = Report(name=name,
                            description=description,
                            url=file_path,
                            user_id=current_user.id,
                            file_name=filename
                            )
            db_session.add(report)
            db_session.commit()
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            payload = {
                        "message": "Upload successful.",
                        "filename": filename,
                        "reportname": name,
                        "description": description,
                        "user": current_user.email
                        }
            return render_json(payload, 200)
        return render_json({"error": "Invalid file."}, 422)


class Read(Resource):
    '''
    This class represents the reading of a report.
    auth_token is necessary.

    method: GET
    url: /api/v1/report/read/<report_id>

    example httpie request:
        http GET http://127.0.0.1:5000/api/v1/report/read/1 \
            Authentication-Token:GET_AUTH_TOKEN_WITH_LOGIN_API_AND_PASTE_HERE

    response:
        {
            "meta": {
                "code": 200
            },
            "response": {
                "created_at": "2022-02-23T02:10:56",
                "description": "This is description",
                "file_name": "example.pdf",
                "id": 1,
                "name": "This is report name",
                "updated_at": "2022-02-23T02:10:56",
                "url": "/path/to/file/example.pdf",
                "user": 1
            }
        }
    '''
    @staticmethod
    @auth_required()
    def get(report_id):
        '''
        This method is used for reading a report.
        '''
        report = (Report.query.
                  filter_by(id=report_id, user_id=current_user.id).
                  first())
        print(report)
        if report is None:
            return render_json({'error': 'Report not found or invalid.'}, 404)
        payload = ReportSchema().dump(report)
        return render_json(payload, 200)


class UpdateData(Resource):
    '''
    This class represents the updating of a report.
    auth_token is necessary.

    method: PUT
    url: /api/v1/report/update/<report_id>
    required input parameters:
        name: report name
        description: report description

    example httpie request:
        http PUT http://127.0.0.1:5000/api/v1/report/update/1 \
            Authentication-Token:GET_AUTH_TOKEN_WITH_LOGIN_API_AND_PASTE_HERE \
            name='This is report name' \
            description='This is report description'

    response:
        {
            "meta": {
                "code": 200
            },
            "response": {
                "message": "Report uploaded successfully",
                "reportname": "This is report name",
                "user": example@example.com
            }
        }
    '''
    @staticmethod
    @auth_required()
    def put(report_id):
        '''
        This method is used for updating a report.
        '''
        try:
            name, description = (
                request.json['name'].strip(),
                request.json['description'].strip()
            )
        except KeyError:
            return render_json({"error": "Invalid input."}, 422)

        report = (Report.query.
                  filter_by(id=report_id, user_id=current_user.id).
                  first())
        if name:
            report.name = name
        if description:
            report.description = description
        db_session.commit()
        payload = {
            "message": "Upload successful.",
            "reportname": name,
            "user": current_user.email
            }
        return render_json(payload, 200)


class UpdateFile(Resource):
    '''
    This class represents the updating of a report.
    auth_token is necessary.

    method: PUT
    url: /api/v1/report/update/<report_id>
    required input parameters:
        name: report name
        description: report description

    example httpie request:
        http -f PUT http://127.0.0.1:5000/api/v1/report/update/1 \
            Authentication-Token:GET_AUTH_TOKEN_WITH_LOGIN_API_AND_PASTE_HERE \
            file@/path/to/file/example.pdf

    response:
        {
            "meta": {
                "code": 200
            },
            "response": {
                "message": "Report uploaded successfully",
                "filename": "example.pdf",
                "user": example@example.com
            }
        }
    '''
    @staticmethod
    @auth_required()
    def put(report_id):
        '''
        This method is used for updating a report.
        '''
        file = (
            request.files['file']
        )

        report = (Report.query.
                  filter_by(id=report_id, user_id=current_user.id).
                  first())
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            report.url = file_path
            report.file_name = filename
            db_session.commit()
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            payload = {
                        "message": "Upload successful.",
                        "filename": filename,
                        "user": current_user.email
                        }
            return render_json(payload, 200)
        return render_json({"error": "Invalid file."}, 422)


class Download(Resource):
    '''
    This class represents the downloading of a report.
    auth_token is necessary.

    method: GET
    url: /api/v1/report/download/<report_id>


    HTTPIE does not support a binary download.
        ref: https://httpie.io/docs/cli/binary-data

    example curl request:
        curl -H  "Authentication-Token: \
            GET_AUTH_TOKEN_WITH_LOGIN_API_AND_PASTE_HERE" \
            http://127.0.0.1:5000/api/v1/report/download/1 \
            -o FILENAME_THAT_YOU_SPECIFY

    If you do not specify the output file,
    you will get the following warning message.

    ```
    Warning: Binary output can mess up your terminal. Use "--output -" to tell
    Warning: curl to output it to your terminal anyway, or consider "--output
    Warning: <FILE>" to save to a file.
    ```
    '''
    @staticmethod
    @auth_required()
    def get(report_id):
        '''
        This method is used for downloading a report.
        '''
        report = (Report.query.
                  filter_by(id=report_id, user_id=current_user.id).
                  first())
        return send_from_directory('./static/uploads',
                                   report.file_name,
                                   as_attachment=True)


class Delete(Resource):
    '''
    This class represents the deleting of a report.
    auth_token is necessary.

    method: DELETE
    url: /api/v1/report/delete/<report_id>

    example httpie request:
        http DELETE http://127.0.0.1:5000/api/v1/report/delete/1 \
            Authentication-Token:GET_AUTH_TOKEN_WITH_LOGIN_API_AND_PASTE_HERE

    response:
        {
            "meta": {
                "code": 200
            },
            "response": {
                "message": "Report deleted successfully"
            }
        }
    '''

    @staticmethod
    @auth_required()
    def delete(report_id):
        '''
        This method is used for deleting a report.
        '''
        report = (Report.query.
                  filter_by(id=report_id, user_id=current_user.id).
                  first())
        db_session.delete(report)
        db_session.commit()
        payload = {
                    "message": "Report deleted successfully"
                    }
        return render_json(payload, 200)
