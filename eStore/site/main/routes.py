from flask import render_template, request, Blueprint
from eStore.models import Products
from sqlalchemy.exc import OperationalError

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    try:
        page = request.args.get('page', 1, type=int)
        products = Products.query.order_by(Products.rating.desc()).paginate(page=page, per_page=5)
        print('products length = ' + str(len(products.items)))
        print('products dict = ' + str(products.total))
        return render_template('index.html', products=products)

    except Exception as e:
        print('Exception error : ' + str(e))
        print('Exception type : ' + str(type(e)))
        return render_template('exception.html', e=e)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
