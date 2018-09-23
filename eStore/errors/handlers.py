from flask import Blueprint, render_template, request

from eStore import db
from eStore.api.errors import error_response as api_error_response


errors = Blueprint('errors', __name__)

def wants_json_response():
    # print(f"request.accept_mimetypes {type(request.accept_mimetypes)}")
    # print(f"accept_mimetypes.application/json {type(request.accept_mimetypes['application/json'])}")
    # print(f"accept_mimetypes.text/html {request.accept_mimetypes['text/html']}")

    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']


@errors.app_errorhandler(404)
def error_404(error):
    if wants_json_response():
        return api_error_response(404)
    return render_template('errors/404.html'), 404


@errors.route('/errors/404.html')
def error_404_page():
    return render_template('errors/404.html')

@errors.app_errorhandler(403)
def error_403(error):
    if wants_json_response():
        return api_error_response(403)
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template('errors/500.html'), 500
