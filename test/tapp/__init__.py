from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
from flask_mail import Mail  
from tapp.config import Config 


print( f"--- CONFIG FILE ---\n{Config() }") 

# create associated db instance
# schema: User --* Posts
db = SQLAlchemy(  ) 

##password hash
bcrypt = Bcrypt(  ) 

## login and user manager
login_manager = LoginManager( ) 
login_manager.login_view = 'users.login' ##indicate login route 
login_manager.login_message_category = 'info' 


## mail server @ GMAIL example 
mail = Mail( ) 


## dummy data
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



def create_app(config_obj=Config):
    ### The app
    app = Flask(__name__) 
    app.config.from_object( config_obj ) 

    db.init_app( app )
    bcrypt.init_app( app )
    login_manager.init_app( app )
    mail.init_app( app )

    ### Work with Blueprints 
    # from tapp import routes 
    from tapp.main.routes import main 
    from tapp.users.routes import users 
    from tapp.posts.routes import posts 

    app.register_blueprint( main  )
    app.register_blueprint( users  )
    app.register_blueprint( posts  )

    return app 