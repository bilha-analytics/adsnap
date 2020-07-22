import os

class Config():  
    ### Secret key to protect agains css and other attacks
    ##TODO: autogen ONCE with secrets and save config
    # import secrets
    # sec = secrets.token_hex(16)
    SECRET_KEY = os.environ.get('SECRET_KEY', '3cd2d047c7d6579da21bbabf362f165e')

    ### Using sql-lite db for now else set to approprite production uri
    SQLALCHEMY_DATABASE_URI  =  os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///test_site.db' ) 

    ## mail server @ GMAIL example 
    MAIL_SERVER  = 'smtp.googlemail.com'
    MAIL_PORT  = 587
    MAIL_USE_TLS  = True  
    MAIL_USERNAME  = os.environ.get('EMAIL_USER', 'bee@goat.com')
    MAIL_PASSWORD  = os.environ.get('EMAIL_PASS', '123')

    def __str__(self):
        return f"""
SECRET_KEY:              {self.SECRET_KEY}
SQLALCHEMY_DATABASE_URI: {self.SQLALCHEMY_DATABASE_URI}
MAIL_SERVER:             {self.MAIL_SERVER}
MAIL_PORT:               {self.MAIL_PORT}
MAIL_USE_TLS:            {self.MAIL_USE_TLS}
MAIL_USERNAME:           {self.MAIL_USERNAME}
MAIL_PASSWORD:           {self.MAIL_PASSWORD}

        """  