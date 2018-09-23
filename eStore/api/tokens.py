from flask import g, jsonify, request

from eStore import db
from eStore.api import api
from eStore.api.auth import basic_auth, token_auth


@api.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    # print(f"get_token - request.headers : \n{request.headers}")
    token = g.current_user.get_token()
    db.session.commit()

    return jsonify({'token' : token,
                    'email id' : g.current_user.email_id})

@api.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()

    return '', 204
