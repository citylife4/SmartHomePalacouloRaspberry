from homedash import blueprint, login_manager
from homedash.forms import LoginForm
from homedash.models import User
from flask_login import login_user, logout_user, current_user, login_required
from flask import redirect, request, session, render_template, url_for, flash


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
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
        print("username invalid: " + username)
        flash('Username is invalid', 'error')
        return redirect(url_for('homedash.login'))
    if not registered_user.check_password(password):
        print("password invalid: " + password)
        flash('Password is invalid', 'error')
        return redirect(url_for('homedash.login'))
    login_user(registered_user)
    print("Valid " + username)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('homedash.index'))


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homedash.index'))
