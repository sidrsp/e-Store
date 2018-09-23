from flask import g, request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from eStore.CONSTANTS import API_RESPONSE_CODES
from eStore.models import Users
from eStore.api.errors import error_response


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verfiy_password(email_id, password):
    # print(f"verfiy_password - request.headers : \n{request.headers}")
    user = Users.query.filter_by(email_id=email_id).first()
    if user is None:
        return False

    g.current_user = user
    return user.check_password(password)

@basic_auth.error_handler
def basic_auth_error():
    return error_response(API_RESPONSE_CODES.UNAUTHORIZED_ERROR_STATUS_CODE)

@token_auth.verify_token
def verify_token(token):
    # print(f"verify_token - request.headers : {request.headers}")
    # print(f"token from client : {token}")
    g.current_user = Users.check_token(token)
    return g.current_user is not None

@token_auth.error_handler
def token_auth_error():
    return error_response(API_RESPONSE_CODES.UNAUTHORIZED_ERROR_STATUS_CODE)