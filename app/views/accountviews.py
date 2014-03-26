from flask import render_template, request, session, \
                  abort, redirect, url_for
from app.dbmodels import User
from app.util import getsalt, createhash
from app.db import db
from app import app


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
            if createhash(user_exists.salt,password) == user_exists.password:

                session['username'] = user_exists.uname
                session['role'] = user_exists.role

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

@app.route('/roles', methods=['GET', 'POST'])
def roles():
    
    try:
        if session['isadmin'] == False: 
            abort(401)
    except:
        return redirect(url_for("home"))

    username = request.args.get("username")
    newrole = request.args.get("newrole")

    if username and newrole:
        
        if newrole not in ["Admin", "Guest", "Sales"]:
            abort(401)

        user_exists = User.query.filter_by(uname=username).first()

        if not user_exists:
            abort(401)
        
        if user_exists.role == "Admin" and newrole != "Admin":
            user_exists.isadmin = 0

        user_exists.role = newrole

        if user_exists.role == "Admin":
            user_exists.isadmin = 1
            
        db.session.commit()

    return render_template('roles.html', User=User)

@app.route('/register', methods=['GET', 'POST'])
def register():

    #Don't allow signed in users to acces this page
    if 'username' in session: redirect(url_for("home"))
    
    if request.method == "POST":

        checkuser = request.form['username']
        password = request.form['password']
        checkpass = request.form['check']

        #Check if user already exists
        user_exists = User.query.filter_by(uname=checkuser).first()

        if not user_exists and password == checkpass:
            #If user is not found then go ahead and create the user
            #using the supplied form data
            salt = getsalt() 
            passhash = createhash(salt,password)
            #Do not allow the new user to be an admin default to guest
            newuser = User(checkuser, salt, passhash, "Guest", 0)            
            db.session.add(newuser)
            db.session.commit()

            return render_template('index.html', msg="Registration Successful")

    return render_template('register.html', msg="")

