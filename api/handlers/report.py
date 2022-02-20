import os
from flask import request, send_from_directory
from pathlib import Path
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
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class List(Resource):
    @staticmethod
    @auth_required()
    def get():
        reports = Report.query.filter_by(user_id=current_user.id).all()
        payload = ReportSchema(many=True).dump(reports)
        return render_json(payload, 200)


class Upload(Resource):
    @staticmethod
    @auth_required()
    def post():
        try:
            name, description, file = (
                    request.form['name'].strip(),
                    request.form['description'].strip(),
                    request.files['file'],
            )
        except Exception:
            return render_json({"error": "Invalid input."}, 422)

        if file is None:
            return render_json({"error": "Invalid input."}, 422)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
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
                        "user": current_user.email
                        }
            return render_json(payload, 200)
        else:
            return render_json({"error": "Invalid file."}, 422)


class Read(Resource):
    @staticmethod
    @auth_required()
    def get(id):
        report = (Report.query.
                  filter_by(id=id, user_id=current_user.id).
                  first())
        payload = ReportSchema(many=True).dump(report)
        return render_json(payload, 200)


class Download(Resource):
    @staticmethod
    @auth_required()
    def get(id):
        report = (Report.query.
                  filter_by(id=id, user_id=current_user.id).
                  first())
        return send_from_directory('./static/uploads',
                                   report.file_name,
                                   as_attachment=True)
