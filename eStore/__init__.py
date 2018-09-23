import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from eStore.CONSTANTS import CONSTANTS

from eStore.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):

    app = Flask(__name__, template_folder=CONSTANTS.TEMPLATE_FOLDER, static_url_path=CONSTANTS.STATIC_URL_PATH)


    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from eStore.site.users.routes import users
    from eStore.site.products.routes import products
    from eStore.site.posts.routes import posts
    from eStore.site.main.routes import main
    from eStore.errors.handlers import errors

    from eStore.site.admin.routes import admin
    from eStore.api import api

    app.register_blueprint(users)
    app.register_blueprint(products)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(api, url_prefix='/api')

    return app
