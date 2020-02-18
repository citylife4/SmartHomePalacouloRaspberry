import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))


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
