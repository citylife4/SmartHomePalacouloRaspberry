import socket

from datetime import datetime

from flask import url_for, redirect, render_template, request, jsonify
from flask_login import login_required

from config import Config

from homedash import db
from homedash.main import blueprint
from homedash.models import PortoDoorStatus, PalacouloDoorStatus
from homedash.socket_connection.protocol import send_open
from homedash.main.forms import DateForm
from homedash.main.pi_utils import measure_temp



from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import AjaxDataSource


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return redirect(url_for('homedash.overview'))


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/dashboard/overview')
@login_required
def overview():
    door = PalacouloDoorStatus.query.order_by(PalacouloDoorStatus.id.desc()).first()
    plots = [make_ajax_plot()]
    return render_template('dashboard.html',
                           plots=plots,
                           status=door.door_status,
                           curr=1)


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
    door = PalacouloDoorStatus.query.order_by(PalacouloDoorStatus.id.desc()).first()
    DEBUG = 1
    door_status = door.door_status

    if door_status is 0:
        print("Opening")
        send_open()
    elif door_status is 1:
        print("Still Opening")
    elif door_status is 2:
        print("Closing")
        send_open()
    elif door_status is 3:
        print("Still closing")

    if DEBUG:
        door_status += 1
        if door_status == 4:
            door_status = 0

    new_door_status = PalacouloDoorStatus(date=datetime.now(), door_status=door_status)
    db.session.add(new_door_status)
    db.session.commit()
    return redirect(url_for('homedash.overview'))

@blueprint.route('/dashboard/util/graph_temperature/', methods=['POST'])
@login_required
def graph_temperature():
    #TODO: Check how to fix below code
    x = datetime.now().strftime("%S")
    y = measure_temp()
    return jsonify(x=[x], y=[y])

@blueprint.route('/dashboard/util/gauge_temperature/', methods=['POST'])
@login_required
def gauge_temperature():
    #TODO: Check how to fix below code
    temp = measure_temp()
    return jsonify(temp=[temp])

@blueprint.route('/dashboard/<location>/date/', methods=['GET', 'POST'])
@login_required
def porto_overview(location):

    form = DateForm()
    value = 0

    submit_date = form.dt.data.strftime('%x') if form.validate_on_submit() else datetime.now().strftime('%x')
    door_status = PalacouloDoorStatus.query.all() if "palacoulo" in location else PortoDoorStatus.query.all()
    door = PalacouloDoorStatus.query.order_by(PalacouloDoorStatus.id.desc()).first()
    plots = [make_plot()]
    print(plots)

    for row in door_status:
        if row.date.strftime('%x') in submit_date:
            value = 1

    #print(submit_date)
    #print(location)
    #print(door_status)

    if not door_status:
        print("Problems")
        #abort(404)

    #pagination = Pagination(date, Config.PER_PAGE, count)
    return render_template('table_date_overview.html' ,
                           status=door.door_status,
                           type=location,
                           form=form,
                           submit_date=submit_date,
                           door_table=door_status,
                           value=value,
                           plots=plots)

def make_plot():
    plot = figure(plot_height=300, sizing_mode='scale_width')

    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = [2**v for v in x]

    plot.line(x, y, line_width=4)

    script, div = components(plot)
    return script, div

def make_ajax_plot():
    source = AjaxDataSource(
        data_url=request.url_root + 'dashboard/util/graph_temperature/',
        polling_interval=2000,
        mode='append'
    )

    source.data = dict(x=[], y=[])

    plot = figure(x_axis_type='datetime', plot_height=300, sizing_mode='scale_width')
    plot.line('x', 'y', source=source, line_width=4)

    script, div = components(plot)
    return script, div