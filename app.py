from flask import Flask,render_template,request,redirect,url_for,flash,g
from sqlalchemy.orm import sessionmaker
from models.models import Base,User,Product,ProductItem,DATABASE, initialize
from sqlalchemy import exists
from forms import AccountForm
from controllers import AccountController
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import LoginManager,login_user, logout_user,login_required,current_user 

DEBUG  = True
PORT = 8080
HOST = '0.0.0.0'


#Set re-createtable to True to create tables. This is set excuted onnce.
re_createTable = False
 

#Database engine settings imported from module models
engine = DATABASE
Base.metadata.bind = (engine)

#DbSEssion from alchemy provide user with a database connection session.
#Allowing queries and manipulation. 
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

#To instanciate a session, flask use secret key to encryt cookies and session.
#Key the key secret please.
app.secret_key = 'Wamayyataqillahayajallahumakhraja!'

#Login_manager is used for user recognition on the website.
#It retain user autheticity between page request . It tells each page whether user is aiutheticated, anonymous, or admin as we are going to add later
login_manager = LoginManager()
login_manager.init_app(app)

#The login_view below is set to login. This tells Login_manager to send user back to login Page when
#he try to access a page that requires authentication
login_manager.login_view = 'login'

#Login_manager loader is called when creating user_login. It returns the user identitity to the login_manager.
@login_manager.user_loader
def load_user(userid):
    return session.query(User).get(int(userid))

    
@app.route('/',methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    formLogin = AccountForm.LoginForm()
    if request.method == 'GET' :
        return render_template('index.html',formLogin=formLogin)
    if request.method == 'POST' :
        if request.form.get('login', None)  == 'Login' :
            return AccountController.authenticatePopUpLogin(formLogin,'index')
            


@app.route('/accountsuccess',methods=['GET', 'POST'])
def accountsuccess():
    """ To address user pop up login , we have to pass formLogin to each page """
    formLogin = AccountForm.LoginForm()
    if request.method == 'GET' :
        return render_template('accountsuccess.html',formLogin=formLogin)
    if request.method == 'POST' :
        if request.form.get('login', None)  == 'Login' :
            return AccountController.authenticatePopUpLogin(formLogin,'index')


@app.route('/about',methods=['GET', 'POST'])
def about():
    """ To address user pop up login , we have to pass formLogin to each page """
    formLogin = AccountForm.LoginForm()
    if request.method == 'GET' :
        return render_template('about.html',formLogin=formLogin)
    if request.method == 'POST' :
        if request.form.get('login', None)  == 'Login' :
            return AccountController.authenticatePopUpLogin(formLogin,'about')
        

@app.route('/checkout',methods=['GET', 'POST'])
def checkout():
    """ To address user pop up login , we have to pass formLogin to each page """
    formLogin = AccountForm.LoginForm()
    if request.method == 'GET' :
        return render_template('checkout.html',formLogin=formLogin)
    if request.method == 'POST' :
        if request.form.get('login', None)  == 'Login' :
            return AccountController.authenticatePopUpLogin(formLogin,'checkout')
    

@app.route('/collections',methods = ['GET','POST'])
def collections():
    """ To address user pop up login , we have to pass formLogin to each page """
    formLogin = AccountForm.LoginForm()
    if request.method == 'GET' :
        return render_template('collections.html',formLogin=formLogin)
    
    if request.method == 'POST' :
        if request.form.get('login', None)  == 'Login' :
            return AccountController.authenticatePopUpLogin(formLogin,'collections')
            


@app.route('/contact',methods = ['GET','POST'])
def contact():
    """ To address user pop up login , we have to pass formLogin to each page """
    formLogin = AccountForm.LoginForm()
    if request.method == 'GET' :
        return render_template('contact.html',formLogin=formLogin)
    
    if request.method == 'POST' :
        if request.form.get('login', None)  == 'Login' :
            return AccountController.authenticatePopUpLogin(formLogin,'contact')
            

#Create Account view. The first if, If the request type is GET , return our form Else Post a form.
@app.route('/createaccount', methods = ['GET','POST'])
def createaccount():
    form = AccountForm.RegisterForm()
    formLogin = AccountForm.LoginForm()
    if request.method =='GET':
        return render_template('createaccount.html',form=form,formLogin=formLogin)
    if request.method =='POST':
        if request.form.get('login', None)  == 'Login' :
            return AccountController.authenticatePopUpLogin(formLogin,'index')
        return AccountController.createuser(form=form, formLogin=formLogin)

@app.route('/lookbook',methods = ['GET','POST'])
def lookbook():
    """ To address user pop up login , we have to pass formLogin to each page """
    formLogin = AccountForm.LoginForm()
    if request.method == 'GET' :
        return render_template('lookbook.html',formLogin=formLogin)
    
    if request.method == 'POST' :
        if request.form.get('login', None)  == 'Login' :
            return AccountController.authenticatePopUpLogin(formLogin,'lookbook')



@app.route('/product',methods=['GET', 'POST'])
def product():
    """ To address user pop up login , we have to pass formLogin to each page """
    formLogin = AccountForm.LoginForm()
    if request.method == 'GET' :
        return render_template('product.html',formLogin=formLogin)
    
    if request.method == 'POST' :
        if request.form.get('login', None)  == 'Login' :
            return AccountController.authenticatePopUpLogin(formLogin,'product')


@app.route('/terms',methods=['GET', 'POST'])
def terms():
    """ To address user pop up login , we have to pass formLogin to each page """
    formLogin = AccountForm.LoginForm()
    if request.method == 'GET' :
        return render_template('terms.html',formLogin=formLogin)
    
    if request.method == 'POST' :
        if request.form.get('login', None)  == 'Login' :
            return AccountController.authenticatePopUpLogin(formLogin,'terms')


@app.route('/login', methods = ['GET','POST'])
def login():
    form = AccountForm.LoginForm()
    if request.method == 'GET' :
        # Check if user is already logged in, return login page if not, otherwise index
        if g.user.is_authenticated() == False:
            return render_template('login.html', form=form,formLogin=form)
        if g.user.is_authenticated():
            return redirect(url_for('index'))
            
    return AccountController.authenticate(form = form)
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You 've been logged out!", "success")
    return redirect(url_for('index'))
    
    
    

#The method before is called before each request(i.e GET,POST).
#It you want something to be executed before each request then add it below
@app.before_request
def before_request():
    """Connect to the database connection before each request. """
    g.user = current_user
    

#The method after is called after each request
@app.after_request
def after_request(response):
    """Close database connection after each request. """
    #g.db.close()
    return response
          

if __name__ == '__main__':
    initialize(re_createTable)
    try:
        User.create_user(
            title='MR',
            fname = 'Musa',
            lname = 'Salihu',
            username = 'musa',
            email = 'musa.3@hotmail.com',
            password = 'password',
            address = 'Block 46A-3-4 Siri Ixora Jalan Pjs Seksen 29/11 Shah Alam Malaysia',
            state = 'Selangor',
            is_Admin = True
            )
    except:
        pass
        
    app.run(debug = DEBUG, host=HOST, port= PORT)

    

   
