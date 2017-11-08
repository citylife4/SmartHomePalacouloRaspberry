from config import basedir, FOR_RASP
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

if FOR_RASP:
    from app.gpio_func import setup_gpio


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

if FOR_RASP:
    setup_gpio()

bcrypt = Bcrypt(app)


from app import views, models

