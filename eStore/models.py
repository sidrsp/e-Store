from datetime import datetime, timedelta
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for
from sqlalchemy.orm import backref

from eStore import db, login_manager, bcrypt
from flask_login import UserMixin

import base64
import os


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class Categories(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True, nullable=False)
    category_name = db.Column(db.String(20))
    products = db.relationship('Products', backref='products_categories_br', lazy=True)

    def __repr__(self):
        return f"Categories('{self.category_id}', '{self.category_name}')"


class Products(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True, nullable=False)
    product_name = db.Column(db.String(20), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, db.ForeignKey('ratings.rating_value'), nullable=True, default=0)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.email_id'), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Products('{self.product_id}', '{self.product_name}', '{self.price}')"

    def to_dict(self):
        data = {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'category_id': self.category_id,
            'qty': self.qty,
            'price': self.price,
            'rating': self.rating,
            'seller_id': self.seller_id,
            'description': self.description,
            '_links': {
                'self': '',
                'seller': url_for('api.get_user', email_id=self.seller_id, _external=True)
            }
        }

        return data

class Cart(db.Model):
    __tablename__ = 'cart'
    email_id = db.Column(db.String(50), db.ForeignKey('users.email_id'), primary_key=True, unique=True,
                         nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), primary_key=True, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    sub_total = db.Column(db.Float, nullable=False)
    products = db.relationship('Products', backref='cart_br', lazy=True)

    def to_dict(self, include_email=False):
        data = {
            'product_id': self.product_id,
            'qty': self.qty,
            'sub_total': self.sub_total,
            '_links': {
                'self': ''
            }
        }

        if include_email:
            data['email_id'] = self.email_id

        return data

class Ratings(db.Model):
    __tablename__ = 'ratings'
    rating_value = db.Column(db.Integer, primary_key=True, nullable=False)
    rating_description = db.Column(db.String(10), nullable=False)
    products = db.relationship('Products', backref='products_ratings_br', lazy=True)
    users = db.relationship('Users', backref='users_ratings_br', lazy=True)

class User_type(db.Model):
    __tablename__ = 'user_type'
    type_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    type_name = db.Column(db.String(10), nullable=False, unique=True)
    users = db.relationship('Users', backref='users_type_br', lazy=True)

class Users(db.Model, UserMixin, PaginatedAPIMixin):
    __tablename__ = 'users'
    email_id = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.Integer, db.ForeignKey('user_type.type_id'), nullable=False)
    address_line1 = db.Column(db.Text, nullable=False)
    address_line2 = db.Column(db.Text, nullable=False)
    area = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    rating = db.Column(db.Integer, db.ForeignKey('ratings.rating_value'), nullable=False, default=0)
    products = db.relationship('Products', backref='products_sellers_br', lazy='dynamic')
    cart_collection = db.relationship('Cart', backref='user_br', lazy='dynamic')

    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return f"User('{self.name}', '{self.email_id}', '{self.user_name}', '{self.users_type_br.type_name}')"

    def get_id(self):
        return (self.email_id)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self, include_email=False):
        data = {
            'name': self.name,
            'user_name': self.user_name,
            'password': self.password,
            'user_type': self.user_type,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'area': self.area,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'pincode': self.pincode,
            'phone': self.phone,
            'rating': self.rating,
            '_links': {
                'self': url_for('api.get_user', email_id=self.email_id, _external=True),
                'products': url_for('api.get_products', email_id=self.email_id, _external=True)
            }
        }

        if include_email:
            data['email_id'] = self.email_id

        return data

    def from_dict(self, data, new_user=False):
        for field in ['email_id', 'name', 'user_name', 'address_line1', 'address_line2', 'area', 'city', 'state',
                      'country', 'pincode', 'phone']:
            if field in data:
                setattr(self, field, data[field])

        if new_user and 'password' in data:
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            self.password = hashed_password

    def get_token(self,expires_in=120):
        now = datetime.utcnow()

        if self.token and self.token_expiration > now + timedelta(seconds=20):
            print('active token exists')
            return self.token

        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        print('prev token has expired')
        print(f'new token : {self.token}')
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = Users.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            print(f'invalid token')
            return None
        return user


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
