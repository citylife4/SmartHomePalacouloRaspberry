import sys

from app import app, login_manager, db
from .models import User
from forms import LoginForm

from flask import Flask, request, flash, url_for, redirect, render_template, g
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from config import FOR_RASP

from gpio_func import get_distance_boolean, trigger_door


@app.route('/')
@login_required
def index():
    if FOR_RASP:
        print("ola")
        try:
            distance, open_boolean = get_distance_boolean()
        except:
            print(sys.exc_info()[0])

        if (distance >= 300) or (distance <= 2):
            flash('Atualiza a pagina por favor')

        send_data = {
            'open': open_boolean,
            'distance': distance
        }
    else:
        send_data = {
            'open': True,
            'distance': 'DEBUG'
        }

    return render_template('portao.html', **send_data)


@app.route("/portao/trigger")
@login_required
def changeportao():
    trigger_door()

    distance, openboolean = get_distance_boolean()

    if openboolean:  # is closed
        flash('A fechar')
    else:  # is open
        flash('A abrir')

    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    print 'ola'
    form = LoginForm()
    print 'oi'
    if request.method == 'GET':
        return render_template('LoginForm.html', form=form)

    username = request.form['username']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True

    registered_user = User.query.filter_by(username=username).first()
    print(registered_user)
    if registered_user is None:
        print 'username invalid'
        flash('Username is invalid', 'error')
        return redirect(url_for('login'))
    if not registered_user.check_password(password):
        print 'password invalid'
        flash('Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    print("Valid")
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(id):
    print("asd")
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
