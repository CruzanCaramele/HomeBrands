from flask_wtf import Form
from wtforms import StringField,PasswordField
from wtforms.validators import (DataRequired, Regexp, ValidationError,
                                Email, Length, EqualTo)
from models import Users,Base,DATABASE
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func


engine = DATABASE
Base.metadata.bind = (engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

 

def name_exists(form, field):
    if session.query(Users).filter_by(username==form.data)  :
        raise ValidationError('User with the name already exists !')
    
def email_exists(form, field):
    if session.query(Users).filter_by(email==form.data) :
        raise ValidationError('User with the email already exists !')
    
class RegisterForm(Form):
    fname = StringField('First Name',validators = [ DataRequired() ])
    lname = StringField( 'Last Name',validators = [DataRequired()])
    address = TextField('Address',validators = [DataRequired()])
    lname = StringField('Last Name', validators = [DataRequired()])
    username = StringField('Username',
                           validators = [DataRequired(),
                                         Regexp(r'^[a-zA-Z0-9_]+$',
                                         message = ("Username should be one word , letters,"
                                                    "numbers, and underscore only")),
                                         name_exists])
    email =  StringField('Email',validators = [DataRequired(),Email(),email_exists])
    password = PasswordField('Password',validators = [DataRequired(),Length(min=8),
                                        EqualTo('password2', message = 'Password does not match !')])
    password2 = PasswordField('Confirm Password',validators = [DataRequired()])
                
                
