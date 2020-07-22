from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, 
        SubmitField, BooleanField , TextAreaField, 
        ) #InputRequired
from wtforms.validators import (DataRequired, Length, Email, 
        EqualTo, ValidationError)
from flask_wtf.file import FileField, FileAllowed
from tapp.models import User
from flask_login import current_user


# Registration: Username, email, password 
class RegistrationForm(FlaskForm):
    username = StringField(
                    'Username', ## label 
                    validators=[ ##validation
                        DataRequired(),
                        Length(min=2, max=20)
                    ])

    email = StringField('Email',
                validators=[DataRequired(), Email() ]
            )
    
    password = PasswordField('Password',
                validators=[DataRequired() ]
            )

    confirm_password = PasswordField('Confirm Password',
                validators=[DataRequired(), EqualTo('password') ]
            )

    submit = SubmitField('Sign up')


    def validate_username(self, username):
        user = User.query.filter_by( uname=username.data ).first()  
        if user: ##if exists in db 
            raise ValidationError( f'Username {username.data} is already taken. Choose a different one')


    def validate_email(self, email):
        user = User.query.filter_by( email=email.data ).first()  
        if user: ##if exists in db 
            raise ValidationError('That email is already registered')

# Login
class LoginForm(FlaskForm):
    email = StringField('Email',
                validators=[DataRequired(), Email() ]
            )
    
    password = PasswordField('Password',
                validators=[DataRequired() ]
            )

    remember = BooleanField('Remember me')

    submit = SubmitField('Log in')

        
class UpdateAccountForm(FlaskForm): 
    username = StringField(
                    'Username', ## label 
                    validators=[ ##validation
                        DataRequired(),
                        Length(min=2, max=20)
                    ])

    email = StringField('Email',
                validators=[DataRequired(), Email() ]
            )
    
    profile_pic = FileField('Update profile picture', 
                    validators =[ FileAllowed(['jpg', 'png', 'jpeg'] ) ] 
                )

    submit = SubmitField('Update')


    def validate_username(self, username):
        if username.data != current_user.uname:
            user = User.query.filter_by( uname=username.data ).first()  
            if user: ##if exists in db 
                raise ValidationError( f'Username {username.data} is already taken. Choose a different one')


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by( email=email.data ).first()  
            if user: ##if exists in db 
                raise ValidationError('That email is already registered')


class RequestResetPasswordForm(FlaskForm):
    email = StringField('Email',
                validators=[DataRequired(), Email() ]
            )
    
    submit = SubmitField('Request Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by( email=email.data ).first()  
        if user is None: ##if not exists in db 
            raise ValidationError('No account with that email. Register first')



class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                validators=[DataRequired() ]
            )

    confirm_password = PasswordField('Confirm Password',
                validators=[DataRequired(), EqualTo('password') ]
            )

    submit = SubmitField('Reset Password')


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by( email=email.data ).first()  
            if user: ##if exists in db 
                raise ValidationError('That email is already registered')
