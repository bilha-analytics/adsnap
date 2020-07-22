from flask import ( Blueprint,
        render_template, redirect, url_for, 
        request, flash , abort )
from tapp import db, bcrypt, login_manager, mail 
from tapp.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                RequestResetPasswordForm, ResetPasswordForm)
from tapp.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
from tapp.users.utils import save_profile_pic, send_reset_email

users = Blueprint('users', __name__ ) 


@users.route('/logout' )
def logout():
    logout_user() 
    return redirect( url_for('users.login') ) 



@users.route('/account',  methods=['GET', 'POST'])
@login_required 
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.uname = form.username.data
        current_user.email = form.email.data

        if form.profile_pic.data:
            current_user.img_file = save_profile_pic( form.profile_pic.data ) 

        db.session.commit() 
        flash( f"Your account has been updated", 'success')
        return( redirect(url_for('users.account') ) ) 

    elif request.method == 'GET':
        form.username.data = current_user.uname
        form.email.data = current_user.email 

    profile_pic = url_for('static', filename='profile_pics/'+current_user.img_file ) 

    return render_template('account.html', body_content='Account Details', 
                            profile_pic=profile_pic, zform=form) 



@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect( url_for('main.home') )

    form = RegistrationForm() 
    if request.method == 'POST' and form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash( form.password.data ).decode('utf-8' )
        user = User(uname=form.username.data, email=form.email.data, upass=hashed_pass)
        db.session.add(user)
        db.session.commit() 
        flash( f'Registration successful! Welcome {form.username.data}. You may now login', 'success')
        return redirect( url_for('users.login') )
    return render_template('register.html', body_content='Register', zform=form)


@users.route('/login', methods=['GET', 'POST'])
def login():    
    if current_user.is_authenticated:
        return redirect( url_for('main.home') )

    form = LoginForm() 
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash( user.upass, form.password.data ):
            login_user(user, remember=form.remember.data )
            next_page = request.args.get('next') 
            flash(f"Welcome back {user.uname}" , 'success')
            return  redirect( next_page) if next_page else redirect(url_for('main.home') ) 
        else:
            flash(f"Login Failed. Check email and password", 'danger')

    msg = request.args.get('reset_msg')
    return render_template('login.html', body_content='Login', zform=form, reset_msg=msg) 


#### additional CRUD user
@users.route('/user/<int:user_id>')
def view_user2(user_id): 
    user = User.query.get_or_404( user_id )
    return render_template( 'user.html', title=user.uname, user=user) 


@users.route('/user/<string:uname>')
def view_user(uname): 
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(uname=uname).first_or_404() 
    posts = Post.query.filter_by(author=user)\
           .order_by( Post.dated.desc() )\
           .paginate(page=page, per_page=2)
    return render_template( 'user.html', title=user.uname, user=user, pages=posts) 



@users.route('/reset_pass',  methods=['GET', 'POST'])
def request_reset():
    if current_user.is_authenticated:
        # return redirect(url_for('main.home'))
        msg = send_reset_email(current_user)
        logout_user() 
        return redirect( url_for('users.login', reset_msg=msg) ) 

    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data ).first()
        msg = send_reset_email(user)
        flash(f"Check your email for reset instructions", 'success') 
        return redirect( url_for('users.login', reset_msg=msg) ) 

    return render_template('request_reset.html', title='Request Password Reset', zform=form) 



@users.route('/reset_pass/<token>',  methods=['GET', 'POST'])
def reset_pass(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
        
    user = User.verify_reset_pass_token(token)
    
    if user is None:
        flash( f"Invalid or Expired token", 'warning')
        return redirect( url_for('users.request_reset') ) 

    form = ResetPasswordForm() 
    if request.method == 'POST' and form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash( form.password.data ).decode('utf-8' ) 
        user.upass = hashed_pass 
        db.session.commit() 
        flash( f'Your password has been updated. You may now login', 'success')
        return redirect( url_for('users.login') )

    return render_template('reset_pass.html', title='Request Password Reset', zform=form) 



