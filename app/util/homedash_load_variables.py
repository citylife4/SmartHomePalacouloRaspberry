import sys;
from datetime import date

from sqlalchemy import func

print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend(['/home/jdv/Project/SmartHome_Webserver', '/home/jdv/Project/SmartHome_transmitter',
                 '/home/jdv/Project/SmartHome_Webserver/app/socket_connection',
                 '/home/jdv/Project/SmartHome_Webserver/app/main',
                 '/home/jdv/Project/SmartHome_Webserver/app/Database',
                 '/home/jdv/Project/SmartHome_Webserver/app/auth', '/home/jdv/Project/SmartHome_Webserver'])

from config import Config
from app import create_homedash_app

app = create_homedash_app(Config)
app.app_context().push()
from app.models import PortoDoorStatus, PalacouloDoorStatus

PalacouloDoorStatus.query.all()

door_status = PortoDoorStatus.query.filter(func.date(PortoDoorStatus.date) == date.today()).paginate(1, 55, False)

for row in door_status.items:
    print(row.date.strftime('%x'))
