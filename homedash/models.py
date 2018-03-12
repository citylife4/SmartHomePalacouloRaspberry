from datetime import datetime
from homedash import login, db, bcrypt


class User(db.Model):
    __tablename__ = "users"

    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    password = db.Column('password', db.String(10))
    email = db.Column('email', db.String(50), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DATETIME)
    last_login_date = db.Column('last_login_date', db.DATETIME)
    logged_in_bol = db.Column('logged_in_bol', db.Boolean)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()
        self.last_login_date = datetime.utcnow()
        self.logged_in_bol = False

    @property
    def is_authenticated(self):
        return True
        # return true if user is authenticated, provided credentials

    @property
    def is_active(self):
        return True
        # return true if user is activte and authenticated

    @property
    def is_annonymous(self):
        return False
        # return true if annon, actual user return false

    def change_login_in_status(self, bool):
        self.logged_in_bol = bool
        if not self.logged_in_bol:
            self.last_login_date = datetime.utcnow()
        db.session.commit()
        return self.logged_in_bol

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def check_password(self, password):
        # return check_password_hash(self.password, password)
        return bcrypt.check_password_hash(self.password, password)

    # Todo : add possibility to admins to create and delete users on site

    def __repr__(self):
        return '<User %r>' % self.username


class Door(db.Model):
    __tablename__ = "door"

    id = db.Column('id', db.Integer, primary_key=True)
    date = db.Column('date', db.DATETIME, index=True)
    door_status = db.Column('door_status', db.Boolean)
    door_motion = db.Column('door_motion', db.Boolean)

    def get_door_status(self):
        return self.door_status

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3


class Data(object):
    def __init__(self):
        """
            Sets the default values for the project
        """
        self.door_status = True

    def change_door(self):
        self.door_status = not self.door_status

    def get_door_status(self):
        return self.door_status


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
