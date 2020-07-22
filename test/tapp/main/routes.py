from flask import render_template, request, Blueprint
from tapp import db, bcrypt, login_manager, mail 
from tapp.models import Post
from flask import current_app as app 


main = Blueprint('main', __name__ ) 

@main.route('/')
@main.route('/home')
def home(): 
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by( Post.dated.desc() ).paginate(page=page, per_page=2) #.order_by( Post.id.desc() ) #.all()
    return render_template('home.html', body_content='Welcome Home!', pages=posts)


@main.route('/about' )
def about():
    return render_template('about.html', body_content='About Here')

