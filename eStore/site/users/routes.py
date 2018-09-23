from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from eStore import db, bcrypt
from eStore.models import Users, User_type
from eStore.site.users.forms import (RegistrationForm, LoginForm)
from eStore.site.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


# TODO : delete this later
@users.route("/users")
def view_users():
    user1 = Users.query.filter_by(email_id="siddu.rsp@gmail.com").first()
    admins = User_type.query.filter_by(type_name="admin").first()
    if admins:
        admin_emailID = admins.users[0].email_id
        return admin_emailID



# TODO : delete this later
# @users.route("/addusers")
def addusers():
    from snippets.add_data_db import add_users_table
    add_users_table()
    return "<h1>Added users</h1>"


# TODO : delete this later
# @users.route("/addcat")
def addcat():
    from snippets.add_data_db import add_categories_table
    add_categories_table()
    return "<h1>Added categories</h1>"


# TODO : delete this later
# @users.route("/addprod")
def addprod():
    from snippets.add_data_db import add_products_table
    add_products_table()
    return "<h1>Added products</h1>"



@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(name=form.name.data, email_id=form.email_id.data, user_name=form.user_name.data, password=hashed_password, user_type=2)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email_id=form.email_id.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


