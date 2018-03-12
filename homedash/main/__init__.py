from flask import Blueprint

blueprint = Blueprint('homedash', __name__) #  url_prefix='/homecontrol'

from homedash.main import routes