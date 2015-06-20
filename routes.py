from flask import Flask,render_template

DEBUG  = True
PORT = 8080
HOST = '0.0.0.0'

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
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


@app.route('/createaccount')
def createaccount():
    return render_template('createaccount.html')

@app.route('/lookbook')
def lookbook():
    return render_template('lookbook.html')



@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

if __name__ == '__main__':
    app.run(debug = DEBUG, host=HOST, port= PORT)
