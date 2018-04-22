import socket
from datetime import datetime

from flask import url_for, redirect, render_template, session
from flask_login import login_required

from config import Config
from homedash import db
from homedash.main import blueprint
from homedash.models import Door
from homedash.socket_connection.protocol import send_open
from flask_login import current_user, login_required

"""
@blueprint.before_app_request
def before_request():
    if current_user.is_authenticated:
        urrent_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())
"""


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return redirect(url_for('homedash.overview'))




@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/dashboard/overview')
@login_required
def overview():
    door = Door.query.order_by(Door.id.desc()).first()

    door_status = door.door_status
    door_motion = door.door_motion

    if door_motion:
        if door_status:
            status=0
        else:
            status=1
    else:
        if door_status:
            status=2
        else:
            status=3

    return render_template('dashboard.html', status=status, curr=1)


@blueprint.route('/dashboard/history')
@login_required
def history():
    return render_template('construction.html')


@blueprint.route('/dashboard/control/open_porto_door')
@login_required
def open_porto_door():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((Config.INTERNAL_SERVER, Config.INTERNAL_PORT))
    client.sendall(bytes("This is from Client", 'UTF-8'))
    client.close()

    #ser = serial.Serial('/dev/ttyAMA0', 9600, timeout = 1)
    #ser.write(b'1')

    return redirect(url_for('homedash.overview'))


@blueprint.route('/dashboard/control/garagedoor')
@login_required
def change_garage_door():
    door = Door.query.order_by(Door.id.desc()).first()

    door_status = door.door_status
    door_motion = door.door_motion
    print(door_status)
    print(door_motion)

    if door_motion:
        if door_status:
            print("Still opening")
            to_do = True
            debug = False
        else:
            print("Still closing")
            to_do = False
            debug = False
    else:
        if door_status:
            print("Closing")
            send_open()
            to_do = True #chegned
            debug = True
        else:
            print("Opening")
            send_open()
            to_do = False #cehgne
            debug = True

    new_door_stuts = Door(date=datetime.now(), door_status=to_do, door_motion=debug)
    db.session.add(new_door_stuts)
    db.session.commit()
    return redirect(url_for('homedash.overview'))
