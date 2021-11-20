from flask import Flask
from map import getMap

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/map")
def map():
    return getMap()
