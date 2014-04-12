from flask import render_template, request, session, abort, redirect, url_for
from app.dbmodels import User, OrderInfo
from app.util import getsalt, createhash
from app.db import db
from app import app

@app.route('/')
def home(message = "Welcome to home page!"):
    print message
    if "role" not in session:
        return render_template('index.html',order_count = 1, message=message)
    
    if session["role"] in ["Admin", "Sales"]:
   

        count = OrderInfo.query.filter_by(status="Ready to Process").count()

        return render_template('index.html', order_count=count)
    
    return render_template('index.html',order_count = 2,  message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if 'username' in session:
        abort(401)

    if request.method == "POST": # Check for HTTP POST Request

        checkuser = request.form['username']
        if len(checkuser) > 45 or checkuser == "":
            return redirect(url_for("login"))

        password = request.form['password']
        if len(password) > 128 or password == "":
            return redirect(url_for("login"))

        #Added try/except after triggering exception with random input
        try:
            user_exists = User.query.filter_by(uname=checkuser).first()
        except Exception, e:
            user_exists = None
       
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

        return redirect(url_for("login"))

    return render_template("accounttemps/login.html")

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

    return render_template('accounttemps/roles.html', User=User)

@app.route('/register', methods=['GET', 'POST'])
def register():

    # redirect sign in user to home page
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

            return render_template('index.html', message = "Registration Successful")

    return render_template('accounttemps/register.html')