import sys

import flask_bcrypt

sys.path.insert(0, '/home/jdv/Project/SmartHome_Webserver/')
sys.path.insert(0, '/home/jdv/Project/SmartHome_Webserver/homedash')

from homedash import db
from homedash.models import User

name = 'jdv'
password = 'V,kC[H9jY3E?+c[b'
email = 'delfimvalverde@gmail.com'


u = User(username=name, email=email, password=flask_bcrypt.generate_password_hash(password))
db.session.add(u)
db.session.commit()
