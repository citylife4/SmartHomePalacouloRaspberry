import os, sys


basedir = os.path.abspath(os.path.dirname(__file__))


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class Config(object):
    FOR_RASP = os.path.isfile('/etc/rpi-issue')  # better way???
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'Database/database.db')
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    eprint(SQLALCHEMY_DATABASE_URI)
    INTERNAL_SERVER = "127.0.0.1"
    INTERNAL_PORT = 54897


global q
q = None

