import os
from flask import request
from pathlib import Path
from werkzeug.utils import secure_filename
from flask_restful import Resource
from flask_security import auth_required, current_user, \
                           SQLAlchemySessionUserDatastore
from api.utils import render_json
from api.models import Report, User
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
        return "Hello Flask Restful Example!"


class Upload(Resource):
    @staticmethod
    @auth_required()
    def post():
        # import pdb; pdb.set_trace()
        try:
            file = request.files['file']
        except Exception:
            return render_json({"error": "Invalid input."}, 422)

        if file is None:
            return render_json({"error": "Invalid input."}, 422)

        if file and allowed_file(file.filename):
            # import pdb; pdb.set_trace()
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            report = Report.query.filter_by(name=filename).first()
            if report is None:
                report = Report(name=filename,
                                url=file_path,
                                user_id=current_user.id)
                db_session.add(report)
                db_session.commit()
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                payload = {
                           "message": "Upload successful.",
                           "filename": filename,
                           "filepath": file_path,
                           "user": current_user.email
                           }
                return render_json(payload, 200)
            else:
                return render_json({"error": "File already exists."}, 422)
        else:
            return render_json({"error": "Invalid file."}, 422)
