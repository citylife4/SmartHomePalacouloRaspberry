import sys

sys.path.insert(0, '/home/jdv/Project/SmartHome_Webserver/')
sys.path.insert(0, '/home/jdv/Project/SmartHome_Webserver/app')

from config import Config
from app import create_homedash_app
from app import db
from app.models import User

name = 'admin'
password = 'admin'
email = 'admin@admin.com'

app = create_homedash_app(Config)
app.app_context().push()

u = User(username=name, email=email, admin=1)
u.set_password(password)
db.session.add(u)
db.session.commit()
