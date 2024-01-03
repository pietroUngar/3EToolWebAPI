from .constant import RES_DIR, EXCEL_DIR, os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


class DBHandler:

    dbkey = "None"
    dbpath = None

    def __init__(self, app, main_handler):

        self.app = app
        self.main_handler = main_handler
        self.db = main_handler.db
        self.db_model = self.init_db_class()

    def init_db_class(self):

        class BaseModel(self.db.Model):

            __bind_key__ = "None"

            id = self.db.Column(self.db.Integer, primary_key=True)
            date_created = self.db.Column(self.db.DateTime, default=datetime.utcnow)

        return BaseModel


class UserDBHandler(DBHandler):

    dbkey = "auth_data"
    dbpath = os.path.join(RES_DIR, 'authdb.db')

    def init_db_class(self):

        class User(self.db.Model):

            __bind_key__ = 'auth_data'

            id = self.db.Column(self.db.Integer, primary_key=True)
            email = self.db.Column(self.db.String(100), unique=True)
            password = self.db.Column(self.db.String(100))

        return User


class ExcelFileHandler(DBHandler):

    dbkey = "files_data"
    dbpath = os.path.join(RES_DIR, 'filedatabase.db')
    file_expiration_days = 7

    def init_db_class(self):

        class FileData(self.db.Model):

            __bind_key__ = 'files_data'

            id = self.db.Column(self.db.Integer, primary_key=True)
            date_created = self.db.Column(self.db.DateTime, default=datetime.utcnow)

            filename = self.db.Column(self.db.String(), nullable=False)
            uploader_mail = self.db.Column(self.db.String(), default=None)
            keep_forever = self.db.Column(self.db.Boolean(), default=False)

            @classmethod
            def init_from_request(cls, request):

                f = request.files['file']

                if 'email' in request.form.keys():
                    email = request.form['email']

                else:
                    email = None

                keep_forever = False

                return cls(

                    filename=f.filename,
                    uploader_mail=email,
                    keep_forever=keep_forever

                )

        return FileData

    def save_file(self, request):

        if 'file' in request.files.keys():

            f = request.files['file']
            model = self.db_model
            db_entry = model.init_from_request(request)
            self.db.session.add(db_entry)
            self.db.session.commit()

            save_filename = os.path.join(EXCEL_DIR, "{}.xlsx".format(db_entry.id))

            try:
                f.save(save_filename)

            except:
                pass

    def clear_all_files(self):

        model = self.db_model
        self.db.session.query(model).delete()
        self.db.session.commit()


class MainDBHandler:

    def __init__(self, app):
        self.__init_databases(app)

    def __init_databases(self, app):

        self.app = app

        db_path = os.path.join(RES_DIR, 'appmaindb.db')
        db_uri = 'sqlite:///{}'.format(db_path)
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        app.config['SQLALCHEMY_BINDS'] = {

            UserDBHandler.dbkey: 'sqlite:///{}'.format(UserDBHandler.dbpath),
            ExcelFileHandler.dbkey: 'sqlite:///{}'.format(ExcelFileHandler.dbpath),

        }
        self.db = SQLAlchemy(app)

        self.sub_db_handler = {

            "auth": UserDBHandler(app, self),
            "files": ExcelFileHandler(app, self)

        }


        with app.app_context():

            self.db.create_all()
