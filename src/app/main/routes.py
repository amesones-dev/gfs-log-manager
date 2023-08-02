import flask
from flask import render_template, redirect, url_for, request, current_app, jsonify, flash
from app.main import bp
from flask_login import current_user, login_required

from app.main.forms import GCPCreateLogEntry
from app import gl


@bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    payload = {"status": "OK"}
    return jsonify(payload)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    form = GCPCreateLogEntry()
    if form.validate_on_submit():
        log_level = form.data.get('log_level')
        log_msg = form.data.get('log_msg')
        gl.cloud_log(log_level, log_msg)
        flash('Your log entry has been created')
        return redirect(url_for('main.index'))
    display_app_name = current_app.config.get('FLASK_APP_DISPLAY_NAME')
    return render_template('main/index.html', title=display_app_name, form=form, display_app_name=display_app_name)


@bp.route('/favicon.ico')
def favicon():
    # Alternatively redirect to a static content route
    return flask.send_file('static/pictures/favicon.ico')


@bp.before_request
def before_request():
    scheme = request.headers.get('X-Forwarded-Proto')
    if scheme and scheme == 'http' and request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)
