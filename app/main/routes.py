import time

import threading

from datetime import date
from datetime import datetime

from flask import url_for, redirect, render_template, request, jsonify
from flask_login import login_required
from sqlalchemy import func

from config import Config
from app import db
from app.main import blueprint
from app.main.forms import DateForm
from app.main.pi_utils import measure_temp
from app.models import PortoDoorStatus, PalacouloDoorStatus
from app.socket_connection.protocol import send_open
from app.socket_connection.socket_connection import SocketConnection


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return redirect(url_for('app.overview'))


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/dashboard/overview')
@login_required
def overview():
    # TODO: error if nothing on the Database
    door = PalacouloDoorStatus.query.order_by(PalacouloDoorStatus.id.desc()).first()
    return render_template('dashboard.html',
                           status=door.door_status,
                           curr=1)


@blueprint.route('/dashboard/history')
@login_required
def history():
    return render_template('construction.html')


def open_worker():
    client = SocketConnection(Config.INTERNAL_SERVER, Config.INTERNAL_PORT)
    # client.send_msg("op_<0_1_2_2_0>")
    client.send_msg("op_<0_1_0_2_1>")
    time.sleep(4)
    client.send_msg("op_<0_1_0_2_0>")


@blueprint.route('/dashboard/control/open_porto_door')
@login_required
def open_porto_door():
    t = threading.Thread(target=open_worker)
    t.start()

    # ser = serial.Serial('/dev/ttyAMA0', 9600, timeout = 1)
    # ser.write(b'1')
    #return redirect(request.url)
    # TODO: Fix this
    return redirect(url_for('app.overview'))


@blueprint.route('/dashboard/control/garagedoor')
@login_required
def change_garage_door():
    door = PalacouloDoorStatus.query.order_by(PalacouloDoorStatus.id.desc()).first()
    DEBUG = 1
    print("Ola")
    door_status = door.door_status

    if door_status == 0:
        print("Opening")
        send_open()
    elif door_status == 1:
        print("Still Opening")
    elif door_status == 2:
        print("Closing")
        send_open()
    elif door_status == 3:
        print("Still closing")

    #if DEBUG:
    #    print("asdfasdf")
    #    door_status += 1
    #    if door_status == 4:
    #        door_status = 0

    new_door_status = PalacouloDoorStatus(
        date=datetime.now(),
        door_status=door_status
    )
    db.session.add(new_door_status)
    db.session.commit()

    # TODO: Fix Following
    return redirect(url_for('app.overview'))



@blueprint.route('/dashboard/<location>/date/', methods=['GET', 'POST'])
@login_required
def porto_overview(location):
    value = 0
    form = DateForm()
    page = request.args.get('page', 1, type=int)
    get_date = request.args.get('submit_date', type=str)

    # print("GET:")
    # print(get_date)
    # print("Today:")
    # print(today_string)

    if get_date:
        submit_date = datetime.strptime(get_date, '%Y-%m-%d').strftime('%x')
        submit_date_u = get_date
    else:
        submit_date = form.dt.data.strftime('%x') if form.validate_on_submit() else date.today().strftime('%x')
        submit_date_u = form.dt.data if form.validate_on_submit() else date.today()

    # print(submit_date_u)
    # print(submit_date)

    door_status = \
        PalacouloDoorStatus.query.filter(func.date(PalacouloDoorStatus.date) == submit_date_u).paginate(page, 10, False) \
            if "palacoulo" in location else \
            PortoDoorStatus.query.filter(func.date(PortoDoorStatus.date) == submit_date_u).paginate(page, 10, False)

    door = PalacouloDoorStatus.query.order_by(PalacouloDoorStatus.id.desc()).first()

    if not door_status:
        print("Problems")
        # abort(404)

    # print(door_status.items)
    for row in door_status.items:
        if row.date.strftime('%x') == submit_date:
            #        print("1")
            value = 1

    next_url = url_for('app.porto_overview', location=location, page=door_status.next_num, submit_date=submit_date_u) \
        if door_status.has_next else None
    prev_url = url_for('app.porto_overview', location=location, page=door_status.prev_num, submit_date=submit_date_u) \
        if door_status.has_prev else None

    # pagination = Pagination(date, Config.PER_PAGE, count)
    return render_template('table_date_overview.html',
                           status=door.door_status,
                           value=value,
                           type=location,
                           form=form,
                           submit_date=submit_date,
                           door_table=door_status.items,
                           next_url=next_url,
                           prev_url=prev_url)


# Usefull funtions
