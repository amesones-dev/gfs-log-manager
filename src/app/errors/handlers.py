from flask import render_template, request, jsonify
from app.errors import bp
from werkzeug.http import HTTP_STATUS_CODES
import logging


def json_error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def json_response_preferred():
    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']


@bp.app_errorhandler(401)
def unauthorized_request_status(error):
    error_data = {"url": request.url, "data": error.__str__(), "code": 401}
    logging.error(error_data)
    if json_response_preferred():
        return json_error_response(401)
    return render_template('errors/401.html'), 401


@bp.app_errorhandler(403)
def unauthorized_content_error(error):
    error_data = {"url": request.url, "data": error.__str__(), "code": 403}
    logging.error(error_data)
    if json_response_preferred():
        return json_error_response(403)
    return render_template('errors/403.html'), 403


@bp.app_errorhandler(404)
def not_found_error(error):
    error_data = {"url": request.url, "data": error.__str__(), "code": 404}
    logging.error(error_data)
    if json_response_preferred():
        return json_error_response(404)
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    error_data = {"url": request.url, "data": error.__str__(), "code": 500}
    logging.error(error_data)
    if json_response_preferred():
        return json_error_response(500)
    return render_template('errors/500.html'), 500
