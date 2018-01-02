from flask import request, flash, url_for, redirect, render_template, g
from flask_login import login_user, logout_user, current_user, login_required

from homedash import login_manager, blueprint
from homedash.models import User


@blueprint.route('/')
@login_required
def index():

    send_data = {
        'open': True,
        'distance': 'DEBUG'
    }

    return render_template('portao.html', **send_data)


@blueprint.route("/portao/trigger")
@login_required
def changeportao():
    trigger_door()

    distance, openboolean = get_distance_boolean()

    if openboolean:  # is closed
        flash('A fechar')
    else:  # is open
        flash('A abrir')

    return redirect("/")


@blueprint.route('/login', methods=['GET', 'POST'])
@login_manager.user_loader
def load_user(id):
    print("asd", User.query.get(int(id)))
    return User.query.get(int(id))


@blueprint.before_request
def before_request():
    g.user = current_user
