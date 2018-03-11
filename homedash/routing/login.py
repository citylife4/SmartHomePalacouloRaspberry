from flask import redirect, request, render_template, url_for, flash, abort
from flask_login import login_user, logout_user, current_user

from urllib.parse import urlparse, urljoin
from homedash import blueprint
from homedash.Database.models import User
from homedash.forms import LoginForm


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    print(test_url)
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


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
    next = request.args.get('next')
    #prefix = "/homecontrol"
    #if prefix in next:
    #    print("ola")
    #    next = next.replace(prefix, '')

    print(next)
    if not is_safe_url(next):
        return abort(400)

    print(registered_user.change_login_in_status(True))
    print(request.environ.get('REMOTE_USER'))
    return redirect(next or url_for('homedash.index'))


@blueprint.route('/logout')
def logout():
    print(current_user.change_login_in_status(False))
    logout_user()
    return redirect(url_for('homedash.index'))
