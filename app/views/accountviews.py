from flask import render_template, request, session, abort, redirect, url_for
from app.dbmodels import User, OrderInfo
from app.util import getsalt, createhash
from app.db import db
from app import app

@app.route('/')
def home(message = "Welcome to home page!"):

    # extract messages from redirect URLs
    message = request.args.get('message', '')
    if message == "":
        message = "Welcome to our Car Management System."

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

# character sets for validating registration
lower = [chr(i + 97) for i in range(26)]           # lower-case alphabet (ascii)
upper = [chr(i + 65) for i in range(26)]           # upper-case alphabet (ascii)
digit = [chr(i + 48) for i in range(10)]           # digits
speci = [chr(i + 33) for i in range(14)]           # special char
chars = set(lower + upper + digit)                 # username character set

@app.route('/register', methods=['GET', 'POST'])
def register():

    # redirect signed in user to home page
    if 'username' in session: redirect(url_for("home"))
    
    # user has submitted a registration form
    if request.method == "POST":
        # extract form entries
        username = request.form['username']
        password = request.form['password']
        verified = request.form['check']
        status = 0x0000

        # validate registration
        if not 5 <= len(username) <= 25:                         status += 0x0002  # username must be 5 - 25 characters long
        if set(username) - chars:                                status += 0x0004  # username must contain only letters and digits
        if not 5 <= len(password) <= 25:                         status += 0x0008  # password must be 5 - 25 characters long
        if len(set(password) & set(digit)) < 1:                  status += 0x0010  # must contain digit character
        if len(set(password) & set(upper)) < 1:                  status += 0x0020  # must contain capital character
        if len(set(password) & set(speci)) < 1:                  status += 0x0040  # must contain special character
        if password != verified:                                 status += 0x0080  # password is not verified
        if User.query.filter_by(uname=username).first() != None: status += 0x0100  # username already exist

        # create the user if it does not exist
        if not status:
            salt = getsalt() 
            passhash = createhash(salt,password)
            newuser = User(username, salt, passhash, "Guest", 0)            
            db.session.add(newuser)
            db.session.commit()
            return redirect(url_for("home", message="Registration Sucessful"))
        # report password does not match
        elif status & 0x0080: return redirect(url_for("register", message = "Passwords do not match."))
        # report username already exist
        elif status & 0x0100: return redirect(url_for("register", message = "Username already exist."))
        # report validation error
        else: return redirect(url_for("register", message = "Invalid username or password."))

    # present user with initial registration
    return render_template('accounttemps/register.html')