from flask import Flask
from flask_login import LoginManager
from config import Config,dbconfig

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
#подключение к бд и создание экземпляра

from app import modules, routes

