#==============================================================================
# File: accountviews.py
# Auth: Andrew Calvano / Jim Ching
# Desc: Account management interface
#==============================================================================
from flask import render_template, request, session, abort, redirect, url_for
from app.dbmodels import User, OrderInfo, ServiceInfo
from app.util import getsalt, createhash, validate_table
from app.db import db
from app import app

# form tables (validation purposes)
accountreg_ft = ['username', 'password', 'check']
accountlog_ft = ['username', 'password']
accountroe_ft = ['username', 'newrole']

@app.route('/')
def home():
    'System management home page.'
    # check if user is login
    if "role" not in session:
        return render_template('index.html')
    # user login as admin or sales
    elif session["role"] in ["Admin", "Sales"]:
        return render_template('index.html', order_count = \
            OrderInfo.query.filter_by(status="Ready to Process").count(), \
            service_count = ServiceInfo.query.filter_by(stats=1).count())
    # user login as guest
    elif session["role"] in ["Guest"]:
        return render_template('index.html')

# character sets for validating registration
lower = [chr(i + 97) for i in range(26)]           # lower-case alphabet (ascii)
upper = [chr(i + 65) for i in range(26)]           # upper-case alphabet (ascii)
digit = [chr(i + 48) for i in range(10)]           # digits
speci = [chr(i + 33) for i in range(14)]           # special char
chars = set(lower + upper + digit)                 # username character set

@app.route('/register', methods=['GET', 'POST'])
def register():
    'Register the user by adding an entry to the User table.'
    # redirect signed in user to home page (already register)
    if 'username' in session: return redirect(url_for("home"))
    
    # user has submitted a registration form
    if request.method == "POST":
        if validate_table(accountreg_ft, request.form):
            # extract form entries
            username = request.form[accountreg_ft[0]]
            password = request.form[accountreg_ft[1]]
            verified = request.form[accountreg_ft[2]]
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
                return redirect(url_for("login", message="Registration successful, please sign in!"))
            # report password does not match
            elif status & 0x0080: return redirect(url_for("register", message = "Unable to verified password, please re-enter password."))
            # report username already exist
            elif status & 0x0100: return redirect(url_for("register", message = "{} has already been taken, please choose another username.".format(username)))
            # report validation error
            else: return redirect(url_for("register", message = "Invalid username or password, please re-read the registration form rules."))

    # present user with initial registration
    return render_template('accounttemps/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    'Login the user by setting the session object.'
    # redirect signed in user to home page (already login)
    if 'username' in session: return redirect(url_for("home"))

    # user has submitted credentials
    if request.method == "POST":
        if validate_table(accountlog_ft, request.form):
            # extract form entries
            username = request.form[accountlog_ft[0]]
            password = request.form[accountlog_ft[1]]
            status = 0x0000

            # check whether the fields are empty
            if not 5 <= len(username) <= 25: status += 0x0001  # username must be 5 - 25 characters long
            if not 5 <= len(password) <= 25: status += 0x0002  # password must be 5 - 25 characters long

            # check whether the user exist
            try:
                user_exists = User.query.filter_by(uname=username).first()
            except Exception, e:
                user_exists = None
            if user_exists:
                # check whether the password matches
                if createhash(user_exists.salt,password) == user_exists.password:

                    session['username'] = user_exists.uname
                    session['role'] = user_exists.role

                    if user_exists.isadmin:
                        session['isadmin'] = True
                    else:
                        session['isadmin'] = False
                    status += 0x0010
                else:
                    status += 0x0008
            else:
                status += 0x0004

            if status & 0x0001 or status & 0x0002:
                return redirect(url_for("login", message = 'Short username or password; must be at least length 5 or greater.'))
            elif status & 0x0004 or status & 0x0008:
                return redirect(url_for("login", message = 'Invalid username or password.'))
            elif status & 0x0010:
                return redirect(url_for("home"))

    # present user with initial sign in form
    return render_template("accounttemps/login.html")

@app.route('/roles', methods=['GET'])
def roles():
    'Allow administrators to change the roles of other users.'
    # check if user is login in and check if user is administrator
    if 'isadmin' not in session.keys() or session['isadmin'] == False:
        return redirect(url_for("home"))

    if request.method == 'GET':
        if validate_table(accountroe_ft, request.args):
            username = request.args.get(accountroe_ft[0])
            newrole = request.args.get(accountroe_ft[1])
            message = ''

            # check the role
            if newrole in ['Admin','Sales', 'Guest']:
                # check if user exist
                user_exists = User.query.filter_by(uname = username).first()
                if user_exists == None:
                    message = 'You\'ve modified an invalid user\'s role.'
                # check if user is modifying his own permission level
                elif user_exists.uname == session['username']:
                    message = 'You cannot modify your own permission level.'
                else:
                    # set off administrator flag
                    if user_exists.role == "Admin" and newrole != "Admin":
                        user_exists.isadmin = 0

                    # set new role
                    user_exists.role = newrole

                    # set on administrator flag
                    if user_exists.role == "Admin":
                        user_exists.isadmin = 1
                    
                    # commit the transaction
                    db.session.commit()
                    message = '{} role changed to {}.'.format(user_exists.uname, user_exists.role)
            else:
                message = 'Role action denied; invalid role({}).'.format(newrole)
            return render_template('accounttemps/roles.html', User = User, message = message)

    # present user with initial table
    return render_template('accounttemps/roles.html', User = User)

@app.route('/logout')
def logout():
    'Logout the user by clearing the session object.'
    if 'username' in session: session.clear()
    return redirect(url_for("home"))
