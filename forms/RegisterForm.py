from flask_wtf import Form
from wtforms import StringField,PasswordField,TextAreaField,DateField,SelectField,RadioField,BooleanField
from wtforms.validators import (DataRequired, Regexp, ValidationError,
                                Email, Length, EqualTo)
from models.models import Base,User,Product,ProductItem,DATABASE
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists


engine = DATABASE
Base.metadata.bind = (engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

 

def name_exists(form, field):
    if session.query(exists().where(User.username == field.data)).scalar()  :
        raise ValidationError('User with the username already exists !')
    
def email_exists(form, field):
    if session.query(exists().where(User.email == field.data)).scalar() :
        raise ValidationError('User with the email already exists !')
    
class RegisterForm(Form):
    title = RadioField('Title', choices =[('Mr','Mr'),('Ms','Ms')])
    fname = StringField('First Name',validators = [ DataRequired() ])
    lname = StringField( 'Last Name',validators = [DataRequired()])
    username = StringField('Username',
                           validators = [DataRequired(),
                                         Regexp(r'^[a-zA-Z0-9_]+$',
                                         message = ("Username should be one word , letters,"
                                                    "numbers, and underscore only")),
                                         name_exists])
    email =  StringField('Email',validators = [DataRequired(),Email(),email_exists])
    password = PasswordField('Password',validators = [DataRequired(),Length(min=8),
                                        EqualTo('password2', message = 'Password does not match !')])
    password2 = PasswordField('Re-Enter Password',validators = [DataRequired()])
    address = TextAreaField('Address',validators = [DataRequired()])
    state = SelectField('State', choices=[('us','USA'),('gb','Great Britain'),('ru','Russia')])
                
                
class LoginForm(Form):
    email = StringField('Enter email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Password')
