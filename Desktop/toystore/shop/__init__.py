from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os
import pymysql

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = '017dc53df170bfea63a7e9fcb0f9c367'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://chuong:password@localhost/app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.url_map.strict_slashes = False
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/staff/images')
photos = UploadSet('photos',IMAGES)
configure_uploads(app,photos)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from shop  import routes