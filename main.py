from flask import Flask, redirect, url_for, request, render_template
from flask.globals import current_app
from map import getMap
import database

app = Flask(__name__)
current_user = ""

class History:
       def __init__(self, _type, points, timestamp):
              self.type = _type
              self.points = points
              self.timestamp = timestamp
              #self.location = location 

def compute_history(x):
       print(x)
       if (x[2] == "pick"):
              return History(_type = "Picked up trash at", points = x[3], timestamp = str(x[1]))
       return History(_type = "Reported trash at", points = x[3], timestamp = str(x[1]))

@app.route("/")
def hello_world():
    return redirect('/home')

@app.route("/home", methods = ['GET', 'POST'])
def home():
	global current_user
	if request.method == 'POST':
		if current_user == "":
			return redirect('/login')
		else:
			return redirect('/user/'+current_user)
	return getMap()

@app.route('/login', methods = ['GET', 'POST'])
def login():
	global current_user

	if request.method == 'GET':
		return render_template('login.html') 

	if request.method == 'POST':
		uname = request.form['uname']
		pword = request.form['pword']
		result = database.log_in(uname, pword)
		if result['code']:
			return result['msg']
		current_user = uname
		return redirect('/home')
		

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

@app.route('/user/<username>', methods = ['GET', 'POST'])
def profile(username):
	if request.method == 'POST':
		current_user = ""
		return redirect('/home')
	if request.method == 'GET':
		# log_action("adela", "report", 1)
		# log_action("adela", "pick", 20)
		# add_user("adela", "adela", "Adela Vais", "+490668955844", "Arcisstraße 21, 80333 München")
		user_data = database.get_user(username)
		# print(user_data)
		# history1 = History(_type = "Reported trash at", points = 10, location = "Arcisstrasse")
		# history2 = History(_type = "Picked up trash at", points = 100, location = "Marienplatz")
		history_data = database.get_history(username) # [history1, history2]
		# print(history_data)
		history = list(map(compute_history, history_data))
		# history_points = map(lambda a: a.points, history)
		return render_template(
			'profile.html',
			name = user_data[3],
			# address = "Arcisstraße 21, 80333 München",
			address = user_data[5],
			email = user_data[4],
			phone = user_data[4],
			points = user_data[2], #reduce(lambda a,b: a + b, history_points, 0),
			history = history,
			leng = len(history),
			username = username,
		) 

@app.route('/user/edit/<username>', methods = ['POST', 'GET'])
def edit_user_data(username):
	if request.method == 'GET':
		user_data = database.get_user(username)
		# print(user_data)
		return render_template(
			'edit_profile.html',
			name = user_data[3],
			# address = "Arcisstraße 21, 80333 München",
			address = user_data[5],
			email = user_data[4],
			phone = user_data,
			username = username,
		)
	if request.method == 'POST':
		name = request.form['name']
		# print(name)
		address = request.form['address']
		# print(address)
		email = request.form['email']
		# print(email)
		database.update_user_data(username=username, name=name, address=address, email=email)
		return redirect(url_for('profile', username = username))
