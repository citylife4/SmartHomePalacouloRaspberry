from flask import session, request, render_template
from flask_login import login_user, logout_user, current_user, login_required

from homedash import blueprint, config, dash_app, login_manager


@blueprint.route('/dasboard/settings', methods=['GET', 'POST'])
@login_required
def settings():
    password = 'x' * len(config.password)
    return render_template('settings.html', link=config.link, session=session, config=config, pw=password)
