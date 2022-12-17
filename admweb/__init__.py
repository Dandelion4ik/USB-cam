from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = 'C:/Users/kavia/PycharmProjects/USB-cam/db/upload'
ALLOWED_EXTENSIONS = {'pdf'}

admapp = Flask(__name__)
admapp.secret_key = 'some secret salt'
admapp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

