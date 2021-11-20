from flask import Flask, request, render_template

def getMap():
    return render_template('map.html', markers='', lat=40.712, lon=-74.006)
