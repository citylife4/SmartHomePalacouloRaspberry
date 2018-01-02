from homedash import dash_app, login_manager, blueprint, loc
from flask.helpers import send_from_directory
from flask import redirect, url_for

#Cenas
import homedash.routing.login
import homedash.routing.views

# Provide a secret-key for using WTF-forms
if dash_app.secret_key is None:
    dash_app.secret_key = 'my-secret-key'


# Rule for serving static files
@blueprint.route('/static/<path:filename>')
def static(filename):
    return send_from_directory(loc() + 'static', filename)


# All rules below are for viewing the homedash-pages
#@blueprint.route('/')
#def index():
#    return redirect(url_for('homedash.overview'))

