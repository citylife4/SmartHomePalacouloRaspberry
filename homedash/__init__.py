import os
from sqlalchemy import MetaData
from flask import Blueprint, Flask
from unittest import TestLoader
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from homedash.config import Config

db = None
bcrypt = None
login_manager = None
data = None

# get current location of the project
def loc():
    return os.path.abspath(os.path.dirname(__file__)) + '/'


blueprint = Blueprint('homedash', __name__, template_folder=loc() + 'templates') #  url_prefix='/homecontrol'


def bind(app):
    global dash_app, blueprint, db, bcrypt, login_manager, data

    dash_app = app


    naming_convention = {
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(column_0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
    db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
    db.init_app(app)
    migrate = Migrate(app, db, render_as_batch=True)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'homedash.login'
    bcrypt = Bcrypt(app)

    import homedash.Database

    data = homedash.Database.Data()
    #app.config['SERVER_NAME'] = 'jdvalverde.dynip.sapo.pt'
    import homedash.routing
    app.register_blueprint(blueprint)



# define the blueprint





