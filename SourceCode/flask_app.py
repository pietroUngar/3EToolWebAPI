from .support import MONITORING_DIR, EXCEL_DIR, MainDBHandler
from flask import Flask, render_template, request, Blueprint
import flask_monitoringdashboard as dashboard
from flask_login import LoginManager
import secrets
import os


def create_app(enable_dashboard=False):

    app = Flask(__name__)
    app.config['SECRET_KEY'] = "{}".format(secrets.token_hex())

    main_db_handler = MainDBHandler(app)
    file_handler = main_db_handler.sub_db_handler["files"]

    main = Blueprint('main', __name__)
    auth = Blueprint('auth', __name__)

    if enable_dashboard:
        dashboard.config.init_from(file=os.path.join(MONITORING_DIR, "config.cfg"))

    @app.route('/')
    def home():
        return render_template("home.html")

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():

        if request.method == 'POST':

            file_handler.save_file(request)
            return render_template("home.html")

        return render_template('upload.html')

    @auth.route('/login')
    def login():
        return 'Login'

    @auth.route('/signup')
    def signup():
        return 'Signup'

    @auth.route('/logout')
    def logout():
        return 'Logout'

    return app
