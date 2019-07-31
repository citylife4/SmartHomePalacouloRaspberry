from flask import Blueprint

blueprint = Blueprint('app', __name__) #  url_prefix='/homecontrol'

from app.main import routes