from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
user_login_manager = LoginManager(app)
user_login_manager.login_view = 'login'
user_login_manager.login_message_category = 'info'

from train import routes

def getApp():
    return app