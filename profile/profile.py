from flask import Flask, render_template, redirect, request
from functools import reduce

app = Flask(__name__)

class History:
       def __init__(self, _type, points, location):
              self.type = _type
              self.points = points
              self.location = location 

@app.route('/<username>', methods = ['GET', 'DELETE'])
def profile(user_id):
       if request.method == 'GET':
              history1 = History(_type = "Reported trash in", points = 10, location = "Arcisstrasse")
              history2 = History(_type = "Picked up trash at", points = 100, location = "Marienplatz")
              history = [
                            history1, history2,
                     ]
              history_points = map(lambda a: a.points, history)
              return render_template(
                     'profile.html',
                     name = "Karl Schuller",
                     address = "Arcisstraße 21, 80333 München",
                     email = "karl@tum.de",
                     phone = "+490770366988",
                     points = reduce(lambda a,b: a + b, history_points, 0),
                     history = history,
                     leng = len(history),
                     username = username,
                     ) 
       if request.method == 'DELETE':
              #nothing yet
              return render_template('profile.html')

@app.route('/edit/<username>', methods = ['POST', 'GET'])
def edit_user_data(username):
       if request.method == 'GET':
              return render_template(
                     'edit_profile.html',
                     name = "Karl Schuller",
                     address = "Arcisstraße 21, 80333 München",
                     email = "karl@tum.de",
                     phone = "+490770366988",
                     username = username,
                     )
       if request.method == 'POST':
              name = request.form['name']
              
              return ()



if __name__ == '__main__':
   app.run('127.0.0.1', port=8000, debug = True)