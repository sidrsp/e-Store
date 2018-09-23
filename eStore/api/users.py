from flask import jsonify, request

from eStore.api import api
from eStore.api.auth import token_auth
from eStore.models import Users


@api.route('/users/<email_id>', methods=['GET'])
@token_auth.login_required
def get_user(email_id):
    # print(f"{'='*10} {email_id} {'='*10}")
    # return jsonify(Users.query.filter_by(email_id=email_id).first().to_dict())
    return jsonify(Users.query.get_or_404(email_id).to_dict(include_email=True))


@api.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    # print(f"get_users - request.headers : {request.headers}")
    page = request.args.get('page',1,type=int)
    per_page = min(request.args.get('per_page', 5, type=int), 100)
    print(type(Users.query))
    data = Users.to_collection_dict(Users.query, page, per_page, 'api.get_users')
    return jsonify(data)


@api.route('/users', methods=['POST'])
def create_user():
    pass

@api.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    pass

@api.route('/users/<string:email_id>/products', methods=['GET'])
@token_auth.login_required
def get_products(email_id):
    user = Users.query.get_or_404(email_id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 5, type=int), 100)
    data = Users.to_collection_dict(user.products, page, per_page, 'api.get_products', email_id=email_id)
    return jsonify(data)


@api.route('/users/<string:email_id>/cart', methods=['GET'])
@token_auth.login_required
def get_user_cart(email_id):
    user = Users.query.get_or_404(email_id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 5, type=int), 100)
    data = Users.to_collection_dict(user.cart_collection, page, per_page, 'api.get_products', email_id=email_id)
    return jsonify(data)