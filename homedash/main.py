#!flask/bin/python
from flask import Flask, redirect, url_for
import homedash

import os

dash_app = Flask(__name__)
here = os.path.abspath(os.path.dirname(__file__))
dash_app.config.from_object('config') #TODO Cahnge
homedash.bind(app=dash_app)


def get_session_id():
    # implement here your own custom function
    return '12345'


@dash_app.route('/')
def main():
    print()
    return redirect(url_for('homedash.index'))


if __name__ == '__main__':
    dash_app.run(debug=True, host='0.0.0.0')

