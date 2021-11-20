from flask import Flask, redirect, url_for, request, render_template
from flask.globals import current_app
from map import getMap
import database

app = Flask(__name__)
current_user = ""

@app.route("/")
def hello_world():
    return redirect('/map')

@app.route("/map")
def map():
    return getMap()

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html') 

	if request.method == 'POST':
		uname = request.form['uname']
		pword = request.form['pword']
		result = database.log_in(uname, pword)
		if result['code']:
			return result['msg']
		current_user = uname
		return redirect('/map')
		

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
	if request.method == 'GET':
		return render_template('signup.html')        
	
	if request.method == 'POST':
		fname = request.form['fname']
		lname = request.form['lname']
		email = request.form['email']
		uname = request.form['uname']
		pword = request.form['pword']
		result = database.add_user(uname, pword, fname + " " + lname, email, "")
		if result['code']:
			return result['msg']
		return redirect('/login')
