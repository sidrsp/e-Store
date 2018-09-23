from flask import Blueprint, render_template, request

from eStore.models import Products

products = Blueprint('products', __name__)

@products.route('/product/<int:product_id>')
def product(product_id):
    pname = request.args.get('pname')
    product = Products.query.get_or_404(product_id)
    return render_template('product.html', product=product)


@products.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):

    return render_template('view_cart.html')

