from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
from flask_mail import Mail 
import os

### The app
app = Flask(__name__) 

### Secret key to protect agains css and other attacks
##TODO: autogen ONCE with secrets and save config
# import secrets
# sec = secrets.token_hex(16)
app.config['SECRET_KEY'] = '3cd2d047c7d6579da21bbabf362f165e' 

### Using sql-lite db for now else set to approprite production uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_site.db' 


# create associated db instance
# schema: User --* Posts
db = SQLAlchemy( app ) 

##password hash
bcrypt = Bcrypt( app ) 

## login and user manager
login_manager = LoginManager(app) 
login_manager.login_view = 'users.login' ##indicate login route 
login_manager.login_message_category = 'info' 


## mail server @ GMAIL example 
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# username, password in environment variables  
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

mail = Mail(app) 



posts = [
    {
        'author' : 'Jane Doe',
        'title' : 'Hickory Dickory Dock',
        'content' : 'The mouse went up the clock. The clock struck one. The mouse came down',
        'dated' : '10-Apr-2018',
    },


    {
        'author' : 'John Smith',
        'title' : 'Dichotomy Monotony',
        'content' : 'The quick brown fox jumped over the lazy dogs. yeah.....',
        'dated' : '17-Apr-2018',
    },


    {
        'author' : 'Mwangi Maina',
        'title' : 'Poker Faced!!',
        'content' : 'A ring a ring of roses, A packet full of possies, Atish! Atish! We all fall down!!!',
        'dated' : '10-Apr-2018',
    }
]


### Work with Blueprints 
# from tapp import routes 
from tapp.main.routes import main 
from tapp.users.routes import users 
from tapp.posts.routes import posts 

app.register_blueprint( main  )
app.register_blueprint( users  )
app.register_blueprint( posts  )

