from flask import Flask, render_template, redirect, request, url_for 
from functools import reduce
import sys 
import os
sys.path.append(os.path.abspath(".."))
from database import *

app = Flask(__name__)

_username = "adela"

class History:
       def __init__(self, _type, points, timestamp):
              self.type = _type
              self.points = points
              self.timestamp = timestamp
              #self.location = location 

@app.route('/<username>', methods = ['GET', 'DELETE'])
def profile(username):
       if request.method == 'GET':
              user_data = get_user(_username)
              # history1 = History(_type = "Reported trash at", points = 10, location = "Arcisstrasse")
              # history2 = History(_type = "Picked up trash at", points = 100, location = "Marienplatz")
              history_data = get_history(_username) # [history1, history2]
              history = map(lambda x: history(_type = x.action, points = x.points, timestamp = x.timestamp))
              history_points = map(lambda a: a.points, history)
              return render_template(
                     'profile.html',
                     # name = "Karl Schuller",
                     name = user_data.name,
                     # address = "Arcisstraße 21, 80333 München",
                     address = user_data.address,
                     # email = "karl@tum.de",
                     email = user_data.email,
                     # phone = "+490770366988",
                     phone = user_data.phone,
                     points = reduce(lambda a,b: a + b, history_points, 0),
                     history = history,
                     leng = len(history),
                     username = _username,
                     ) 
       if request.method == 'DELETE':
              #nothing yet
              return render_template('profile.html')

@app.route('/edit/<username>', methods = ['POST', 'GET'])
def edit_user_data(username):
       if request.method == 'GET':
              return render_template(
                     'edit_profile.html',
                     # name = "Karl Schuller",
                     name = user_data.name,
                     # address = "Arcisstraße 21, 80333 München",
                     address = user_data.address,
                     # email = "karl@tum.de",
                     email = user_data.email,
                     # phone = "+490770366988",
                     phone = user_data.phone,
                     username = _username,
                     )
       if request.method == 'POST':
              name = request.form['name']
              address = request.form['address']
              email = request.form['email']
              phone = request.form['phone']
              update_user(username=_username, name=name, address=address, email=email, phone=phone)
              return redirect(url_for('profile', username = _username))


if __name__ == '__main__':
   app.run('127.0.0.1', port=8000, debug = True)