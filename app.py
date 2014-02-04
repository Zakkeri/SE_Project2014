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

    if request.method == "POST": # Check for HTTP POST Request

        checkuser = request.form['username']
        password = request.form['password']

        user_exists = User.query.filter_by(uname=checkuser).first()

        if user_exists:

            #This logic will need to be changed for security reasons
            #We don't want to store passwords in plaintext in the database
            if password == user_exists.password:

                session['username'] = user_exists.uname

                if user_exists.isadmin:
                    session['isadmin'] = True
                else:
                    session['isadmin'] = False
                return redirect(url_for("home"))

    return render_template('login.html')

@app.route('/logout')
def logout():

    #Make sure there is a logged in user
    if 'username' not in session:
        abort(401)

    #Clear session dictionary of user info
    session.clear()

    return redirect(url_for("home"))

@app.route('/register', methods=['GET', 'POST'])
def register():

    #Don't allow signed in users to acces this page
    if 'username' in session: abort(401)
    
    if request.method == "POST":

        checkuser = request.form['username']
        password = request.form['password']
        checkpass = request.form['check']

        #Check if user already exists
        user_exists = User.query.filter_by(uname=checkuser).first()

        if not user_exists and password == checkpass:
            #If user is not found then go ahead and create the user
            #using the supplied form data
             
            #Do not allow the new user to be an admin
            newuser = User(checkuser, password, 0)            

            db.session.add(newuser)
            db.session.commit()

            return render_template('index.html', msg="Registration Successful")

    return render_template('register.html', msg="Error during registration")

if __name__ == "__main__":
    app.run()
