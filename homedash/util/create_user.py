import flask_bcrypt

import os
import sys
import sqlite3

sys.path.insert(0, '/home/jdv/Project/SmartHome_Webserver/')
sys.path.insert(0, '/home/jdv/Project/SmartHome_Webserver/homedash')

import homedash
from homedash import db, Data
from homedash.Database.models import User

name = 'jdv'
password = 'V,kC[H9jY3E?+c[b'
email = 'delfimvalverde@gmail.com'


u = User(username=name, email=email, password=flask_bcrypt.generate_password_hash(password))
db.session.add(u)
db.session.commit()
