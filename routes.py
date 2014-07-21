from flask import *
from functools import wraps

app = Flask(__name__)

app.debug = True;

app.secret_key = 'jK1frnds'

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

@app.route('/')
def home():
	return render_template('home.html')

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
	flash('You were logged out')
	return redirect(url_for('notify'))

@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

@app.route('/log', methods=['GET', 'POST'])
@logout_required
def log():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			session['logged_in']=True
			return redirect(url_for('hello'))
	return render_template('log.html', error=error)

if (__name__ == '__main__'):
	app.run()