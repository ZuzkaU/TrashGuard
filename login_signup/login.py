from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html') 

	if request.method == 'POST':
		uname = request.form['uname']
		pword = request.form['pword']
		return uname

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
		return email

if __name__ == '__main__':
	app.run('127.0.0.1', port=8000, debug = True)
