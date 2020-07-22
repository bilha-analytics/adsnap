from tapp import db, login_manager 
from datetime import datetime 
from flask_login import UserMixin 

from flask import current_app as app

from itsdangerous import TimedJSONWebSignatureSerializer as TSerializer 


### login decorated function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id) ) 

class User(db.Model, UserMixin):
    id = db.Column( db.Integer, primary_key=True)
    uname = db.Column( db.String(20), unique=True, nullable=False)
    email = db.Column( db.String(120), unique=True, nullable=False)
    upass = db.Column( db.String(60), nullable=False)
    img_file = db.Column(db.String(60), nullable=False, default='defaul_profile.jpg') 

    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.uname}', '{self.email}', '{self.img_file}')"

    ## crete and validate timed tokens for update password 
    def get_reset_pass_token(self, expire_secs=1800): #30 minutes
        s = TSerializer( app.config['SECRET_KEY'] , expire_secs)
        return s.dumps( {'user_id': self.id} ).decode( 'utf-8') 

    @staticmethod 
    def verify_reset_pass_token(token):
        s = TSerializer( app.config['SECRET_KEY'] )
        try:
            user_id = s.loads(token)['user_id']
            return User.query.get( user_id ) 
        except:
            return None
            


class Post(db.Model):
    id = db.Column( db.Integer, primary_key=True)
    dated = db.Column( db.DateTime, nullable=False, default=datetime.utcnow )
    title = db.Column( db.String(120), nullable=False)
    content = db.Column( db.Text, nullable=False) 

    author_id = db.Column( db.Integer, db.ForeignKey('user.id') ) 

    def __repr__(self):
        return f"Post('{self.title}', '{self.dated}', '{self.author_id}')"

        