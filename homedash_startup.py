from homedash import create_homedash_app, db
from homedash.models import User

homedash_app = create_homedash_app()

@homedash_app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


if __name__ == '__main__':
    homedash_app.run(debug=True, host='0.0.0.0')