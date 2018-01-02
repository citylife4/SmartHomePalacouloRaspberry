import os
from flask import Blueprint
from unittest import TestLoader
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


dash_app = None
db = None
bcrypt = None
login_manager = None


# get current location of the project
def loc():
    return os.path.abspath(os.path.dirname(__file__)) + '/'


blueprint = Blueprint('homedash', __name__, template_folder=loc() + 'templates')


def bind(app):
    global dash_app, blueprint, db, bcrypt, login_manager

    dash_app = app
    db = SQLAlchemy(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'homedash.login'
    bcrypt = Bcrypt(app)

    import homedash.routing

    app.register_blueprint(blueprint)



# define the blueprint





