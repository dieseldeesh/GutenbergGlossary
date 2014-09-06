from flask import *
from functools import wraps
from webscraper import *
from flask.ext.sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)

app.debug = True;

app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gutenberg.db'

db = SQLAlchemy(app)

from models import *

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if('logged_in' in session):
			return test(*args, **kwargs)
		else:
			flash('You need to log in to view this content')
			return redirect(url_for('notify'))
	return wrap

def logout_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if('logged_in' in session):
			flash('You are already logged in')
			return redirect(url_for('notify'))
		else:
			return test(*args, **kwargs)
	return wrap

@app.route('/', methods=['GET', 'POST'])
def home():
	posts = db.session.query(Annotations).all()
	results=[]
	if request.method == 'POST':
		results=getResults(request.form['query'])
		return render_template('results.html', results=results, searchQuery=request.form['query'])
	return render_template('home.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
	return render_template('results.html')

@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/hello')
@login_required
def hello():
	return render_template('hello.html')

@app.route('/notify')
def notify():
	return render_template('notify.html')

@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	return redirect(url_for('home'))

@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

@app.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
	error = None
	if request.method == 'POST':
		submit = request.form['submit']
		md5er = hashlib.md5()
		md5er.update(request.form['password'])
		hexPass = md5er.hexdigest()
		user = Annotations.query.filter_by(username=request.form['username']).first()
		if submit == "Register":
			if  (not (user is None)) or request.form['username']=='username':
				error = 'The username, ' + request.form['username'] + ', is taken.'
			elif  len(request.form['password'])<8 or request.form['password']=='password':
				error = 'The password you entered is not secure enough.'
			elif  request.form['cpassword'] != request.form['password']:
				error = 'The password you entered was not consistent.'
			else:
				db.session.add(Annotations(request.form['username'],hexPass))
				db.session.commit()
				session['logged_in']=True
				return redirect(url_for('home'))
			return render_template('newlogin.html', error1=None, error2=error)
		else:
			if  user is None:
				error = 'This username, ' + request.form['username'] + ', is not taken yet. Do you want to sign up?'
			elif hexPass != user.password:
				error = 'Invalid Credentials. Please try again.'
			else:
				session['logged_in']=True
				return redirect(url_for('home'))
			return render_template('newlogin.html', error1=error, error2=None)
	return render_template('newlogin.html', error1=None, error2=None)

if (__name__ == '__main__'):
	app.run()