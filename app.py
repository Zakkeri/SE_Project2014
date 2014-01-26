import sys
import os
from flask import Flask, request, session, url_for, \
    abort, render_template, flash, redirect, Response
from dbmodels import * #Importing db interface from sqlalchemy

app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent = True)

app.secret_key = os.urandom(24)

#Setup DB here
db.create_all()

#For creating the inital admin user who will be able
#to create/modify/delete other users inside of the application
if User.query.filter_by(uname="admin").first():
    pass
else:
    admin = User("admin", "test", 1)
    db.session.add(admin)
    db.session.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if 'username' in session:
        abort(401)

    success = 0 # Represents whether the login was sucessful
                # Effects the templating system based on its value

    if request.method == "POST": # Check for HTTP POST Request

        checkuser = request.form['username']
        password = request.form['password']

        user_exists = User.query.filter_by(uname=checkuser).first()

        if user_exists:

            #This logic will need to be changed for security reasons
            #We don't want to store passwords in plaintext in the database
            if password == user_exists.password:

                success = 1 # Value is set to 1 if the correct password is entered
                session['username'] = user_exists.uname

                if user_exists.isadmin:
                    session['isadmin'] = True
                else:
                    session['isadmin'] = False
                return redirect(url_for("home"))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

if __name__ == "__main__":
    app.run()
