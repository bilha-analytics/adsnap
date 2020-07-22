from flask import (Blueprint, 
            render_template, redirect, url_for, 
            request, flash , abort )

from tapp.posts.forms import PostForm 

from tapp import db
from tapp.models import Post
from flask_login import current_user, login_required


posts = Blueprint('posts', __name__ ) 


### --- CRUD @ Post ---- 

@posts.route('/post/new',  methods=['GET', 'POST'])
@login_required 
def new_post():
    form = PostForm()
    if form.validate_on_submit(): 
        post = Post( title=form.title.data, content=form.content.data, author_id=current_user.id )  ##or author=current_user
        db.session.add( post )
        db.session.commit()
        flash( f"Post created successfully!", 'success' )
        return redirect( url_for('main.home') ) 
    return render_template('create_post.html', title='New Post', zform=form , legend='New Post') 

@posts.route('/post/<int:post_id>')
def view_post(post_id): 
    #post = Post.query.get( post_id )
    post = Post.query.get_or_404( post_id )
    return render_template( 'post.html', title=post.title, post=post) 


@posts.route('/post/<int:post_id>/update',  methods=['GET', 'POST'])
@login_required 
def update_post(post_id):
    post = Post.query.get_or_404( post_id ) 

    if post.author != current_user: ## ensure only the owner can edit or del 
        abort(403) 

    form = PostForm()

    if request.method == 'GET': #necessary to avoid confusion with POST entries 
        form.title.data = post.title 
        form.content.data = post.content  

    if form.validate_on_submit(): 
        post.title = form.title.data 
        post.content = form.content.data 
        db.session.commit()
        flash( f"Post updated successfully!", 'success' )
        return redirect( url_for('posts.view_post', post_id=post.id) )  

    return render_template('create_post.html', title='Update Post', 
                zform=form , legend='Update Post') 


@posts.route('/post/<int:post_id>/delete',  methods=[ 'POST'])
@login_required 
def delete_post(post_id):

    post = Post.query.get_or_404( post_id ) 

    if post.author != current_user: ## ensure only the owner can edit or del 
        abort(403) 

    db.session.delete( post ) 
    db.session.commit()
    
    flash( f"Post deleted successfully!", 'success' )
    
    return redirect( url_for('main.home') ) 

