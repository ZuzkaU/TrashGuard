from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/profile')
def profile():
       return render_template('profile.html') 

if __name__ == '__main__':
   app.run('127.0.0.1', port=8000, debug = True)