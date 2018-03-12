from flask import Blueprint

blueprint = Blueprint('auth', __name__)

from homedash.auth import routes