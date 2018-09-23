from flask import Blueprint, render_template, request
from eStore.models import Post

# admin = Blueprint('admin', __name__, template_folder='templates')
admin = Blueprint('admin', __name__)

'''
@admin.route('/')
def homepage():
	return render_template('admin/index.html')
'''

@admin.route('/')
def homepage():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('home.html', posts=posts)