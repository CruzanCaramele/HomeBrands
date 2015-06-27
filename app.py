from flask import Flask,render_template,request,redirect,url_for,flash,g
from sqlalchemy.orm import sessionmaker
from models.models import Base,User,Product,ProductItem,DATABASE, initialize
from sqlalchemy import exists
from forms import RegisterForm
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import LoginManager,login_user, logout_user,login_required,current_user 

DEBUG  = True
PORT = 8080
HOST = '0.0.0.0'
re_createTable = False
 


engine = DATABASE
Base.metadata.bind = (engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

app.secret_key = 'Innalhamdulillah.nahmaduhu.taalanastainubihi.wanastagfiruh!'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    return session.query(User).get(int(userid))

    
@app.route('/',methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.form.get('login', None)  == 'Login' :
        return authenticate()
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/collections')
def collections():
    return render_template('collections.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/createaccount', methods = ['GET','POST'])
def createaccount():
    form = RegisterForm.RegisterForm()
    if request.method =='GET':
        return render_template('createaccount.html',form=form)
    if request.method =='POST':
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
            return render_template('accountsuccess.html', email=request.form['email'])
        return render_template('createaccount.html', form=form)

@app.route('/lookbook')
def lookbook():
    return render_template('lookbook.html')



@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    form = RegisterForm.LoginForm()
    if request.method == 'GET' :
        if g.user.is_authenticated() == False:
            return render_template('login.html', form=form)
        if g.user.is_authenticated():
            return redirect(url_for('index'))
            
    return authenticate(form = form)
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You 've been logged out!", "success")
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = current_user
    #"""Connect to the database connection before each request. """

@app.after_request
def after_request(response):
    """Close database connection after each request. """
    #g.db.close()
    return response


def authenticate(form):
    if form.validate_on_submit():
        try:
            user = session.query(User).filter(User.email == form.email.data).first()
        except :# models.DoesNotExist:
            flash("Your email or password does not match !", "error")
        else :
            if check_password_hash(user.password,form.password.data):
                login_user(user)
                flash("You've been logged in", "success")
                return redirect(url_for('index'))
            else :
                flash("Your email or password does not match !", "error")
    return render_template('login.html',form = form)           

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

    

   
