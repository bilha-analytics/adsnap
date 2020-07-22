import os 
import secrets 
from PIL import Image
from flask import url_for
from tapp import mail 
from flask_mail import Message 

from flask import current_app as app

## save uploaded file. use random hex as filename 
# resize using PIL
def save_profile_pic(form_pic):
    rand_hex = secrets.token_hex(8) 
    _, file_ext = os.path.splitext( form_pic.filename )  
    f_name = f"{rand_hex}{file_ext}"
    print( f_name )
    f_path = os.path.join( app.root_path, 'static/profile_pics', f_name) 
    print( f_path )


    fsize = (125, 125)
    img = Image.open( form_pic) 
    img.thumbnail( fsize )
    #form_pic.save( f_path )
    img.save( f_path )

    return f_name


#### password reset 
def send_reset_email(user):
    token = user.get_reset_pass_token( 60 ) 
    msg = Message('Password Reset Request', 
            sender='noreply@goat.com',
            recipients=[user.email, 'bitzcodie@gmail.com'] )
    msg.body = f'''
To: {user.email}
Re: Password Reset

Dear {user.uname},

To reset your password , visit the following link:
    {url_for('users.reset_pass', token=token, _external=True)}

If you did not make this request, please ignore this email and no change will be made. 
        '''

    print( app.config['MAIL_USERNAME'])
    print( app.config['MAIL_PASSWORD'] )
    #mail.send( msg ) 
    return msg.body 

