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

def compute_history(x):
       print(x)
       if (x[2] == "pick"):
              return History(_type = "Picked up trash at", points = x[3], timestamp = str(x[1]))
       return History(_type = "Reported trash at", points = x[3], timestamp = str(x[1]))


@app.route('/<username>', methods = ['GET'])
def profile(username):
       if request.method == 'GET':
              log_action("adela", "report", 1)
              log_action("adela", "pick", 20)
              # add_user("adela", "adela", "Adela Vais", "+490668955844", "Arcisstraße 21, 80333 München")
              user_data = get_user(_username)[0]
              print(user_data)
              # history1 = History(_type = "Reported trash at", points = 10, location = "Arcisstrasse")
              # history2 = History(_type = "Picked up trash at", points = 100, location = "Marienplatz")
              history_data = get_history(_username) # [history1, history2]
              history = list(map(compute_history, history_data))
              history_points = map(lambda a: a.points, history)
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
                     username = _username,
                     ) 

@app.route('/edit/<username>', methods = ['POST', 'GET'])
def edit_user_data(username):
       if request.method == 'GET':
              user_data = get_user(_username)[0]
              print(user_data)
              return render_template(
                     'edit_profile.html',
                     name = user_data[3],
                     # address = "Arcisstraße 21, 80333 München",
                     address = user_data[5],
                     email = user_data[4],
                     phone = user_data,
                     username = _username,
                     )
       if request.method == 'POST':
              name = request.form['name']
              print(name)
              address = request.form['address']
              print(address)
              email = request.form['email']
              print(email)
              update_user_data(username=_username, name=name, address=address, email=email)
              return redirect(url_for('profile', username = _username))


if __name__ == '__main__':
   app.run('127.0.0.1', port=8000, debug = True)