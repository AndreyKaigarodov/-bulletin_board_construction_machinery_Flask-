from flask import Flask
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)
#подключение к бд и создание экземпляра

from app import modules, routes

