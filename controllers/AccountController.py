from flask import Flask,render_template,request,redirect,url_for,flash,g
from sqlalchemy.orm import sessionmaker
from models.models import Base,User,Product,ProductItem,DATABASE, initialize
from sqlalchemy import exists
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import LoginManager,login_user, logout_user,login_required,current_user
from forms import AccountForm

#Database engine settings imported from module models
engine = DATABASE
Base.metadata.bind = (engine)

#DbSEssion from alchemy provide user with a database connection session.
#Allowing queries and manipulation. 
DBSession = sessionmaker(bind=engine)
session = DBSession()


#authenticate user
def authenticate(form):
    if form.validate_on_submit():
        try:
            user = session.query(User).filter(User.email == form.email.data).first()
        except :# models.DoesNotExist:
            flash("Your email or password does not match !", "error")
        else :
            if check_password_hash(user.password,form.password.data):
                login_user(user, remember = form.remember.data)
                flash("You've been logged in", "success")
                return redirect(url_for('index'))
            else :
                flash("Your email or password does not match !", "error")
                return render_template('login.html',formLogin = form)
    return render_template('login.html',formLogin = form)       

#authenticate pop up login
def authenticatePopUpLogin(formLogin,route):
    if formLogin.validate_on_submit():
        try:
            user = session.query(User).filter(User.email == formLogin.email.data).first()
        except :# models.DoesNotExist:
            return render_template('login.html',form=formLogin,formLogin = formLogin)
            flash("Your email or password does not match !", "error")
        else :
            if check_password_hash(user.password,formLogin.password.data):
                login_user(user, remember = formLogin.remember.data)
                flash("You've been logged in", "success")
                return redirect(url_for(route))
            else :
                flash("Your email or password does not match !", "error")
                return render_template('login.html',form=formLogin,formLogin = formLogin)
                
    return render_template('login.html',form=formLogin,formLogin = formLogin)

#Create Account
def createuser(form, formLogin):
    if form.validate_on_submit():
            flash("yay, you registered!", "success")
            User.create_user(
                title = form.title.data,
                fname = form.fname.data,
                lname = form.lname.data,
                username = form.username.data,
                email = form.email.data,
                password = form.password.data,
                address = form.address.data,
                state = form.state.data,
                is_Admin = True
                )
            return render_template('accountsuccess.html', email=request.form['email'],formLogin=formLogin)
    return render_template('createaccount.html', form=form,formLogin=formLogin)
