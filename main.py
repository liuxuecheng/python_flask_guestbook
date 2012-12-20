import MySQLdb as mdb
import sys

from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash

#db configuration
USERNAME = 'admin'
PASSWORD = '1111'

app = Flask(__name__)
app.config.from_object(__name__)
Flask.secret_key = 'ad'

def connect_db():
	con = mdb.connect('localhost','root','1111','test')
	return con

def init_db():
	return 

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	g.db.close()

#add a message
@app.route('/add', methods=['POST'])
def add():
	if not session.get('logged_in'):
		abort(401)
	g.db.cursor().execute('insert into guestbook (title, text) values(%s, %s)',
			[request.form['title'], request.form['text']])
	g.db.commit()
	flash('new messge was successfully posted')
	return redirect(url_for('show_guestbooklist'))

#login
@app.route('/login', methods=['POST','GET'])
def login():
	error = None
	if request.method == "POST":
		if request.form['username'] != app.config['USERNAME']:
			error = 'invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'invalid password'
		else:
			session['logged_in'] = True
			flash('you were logged in')
			return redirect(url_for('show_guestbooklist'))
	return render_template('login.html', error=error)

#logout
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('you were logged out')
	return redirect(url_for('show_guestbooklist'))

#index
@app.route('/')
def show_guestbooklist():
	cur = g.db.cursor()
	cur.execute('select id,title,text from guestbook order by id desc')
	rows = cur.fetchall()
	guestlist = [dict(id=row[0], title=row[1], text=row[2]) for row in rows]
	return render_template('show_list.html', guestlist=guestlist)

if __name__ == '__main__':
	app.debug = True
	app.run()
