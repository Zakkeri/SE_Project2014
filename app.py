import sys
import binascii
import os
from flask import Flask, request, session, url_for, \
    abort, render_template, flash, redirect, Response
from utilities import *
from dbmodels import * #Importing db interface from sqlalchemy

app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = "/images"
app.config.from_envvar('FLASKR_SETTINGS', silent = True)

app.secret_key = os.urandom(24)

#Setup DB here
db.create_all()

#For creating the inital admin user who will be able
#to create/modify/delete other users inside of the application
if User.query.filter_by(uname="admin").first():
    pass
else:
    salt = getsalt()
    passhash = createhash(salt,"test")
    admin = User("admin", salt, passhash, "Admin", 1)
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

@app.route("/addfeatures", methods=['GET', 'POST'])
def addfeatures():
   
    #If an anonymous user browses this page abort 
    if "role" not in session:
        abort(401)
    
    #Make sure the only users that can access addfeatures are 
    #Admins and Sales
    if session["role"] not in ["Admin", "Sales"]:
        return redirect(url_for("home"))
  
    if request.method == "GET":  
        #Expects a vin during get request, this vin will be the 
        #car in inventory which is queried and modifiable
        vin = request.args.get("vin")

        #Make sure there is an existing car in the car inventory
        #table for the supplied GET vin argument
        car_exists = Car.query.filter_by(vin=vin).first()

        #Make sure there is a VIN Get argument as well as 
        #a matching car row in database
        if not vin or not car_exists:
            abort(404)

        #Now we need to check if we have any existing data
        #in the CarFeatures table for our queried car 
        car_feats_list = CarFeatures.query.filter_by(vin=vin)

        #Constructs a dictionary of available features that can be loaded
        #into view by template using something like feats_dict['performance']
        feats_dict = {feat.feat_type:feat.descr for feat in car_feats_list}

       
        #Need to implement POST logic for when user supplies
        #features data for a car in POST form

        #If there are no existing car_feats then we will supply to
        #Template anyway cause we have logic in template that expects this
        return render_template('addfeature.html', vin=car_exists.vin, feats=feats_dict) 

    #Actually recieve the message from the web view and process accordingly updating or 
    #creating entries in the CarFeatures table
    if request.method == "POST":

#Page for car management accessible by admins and sales
@app.route("/carmanage", methods=['GET','POST'])
def carmanage():
    
    if "role" not in session:
        abort(401)

    #Only allow Admins and Sales Users for accessing
    if session["role"] not in ["Admin", "Sales"]:
        return redirect(url_for("home"))

    #Need to have: Add, Modify, Delete subviews

    action = request.args.get("action")

    if action == "add":
        try:
            if request.method == "POST":
                vin = request.form["vin"]
                make = request.form["make"]
                model = request.form["model"]
                year = request.form["year"]
                retail = request.form["retail"] 

                car_exists = Car.query.filter_by(vin=vin).first()

                if not car_exists:
                    
                    newcar = Car(vin, make, model, year, retail) 
                    db.session.add(newcar)
                    db.session.commit()
        
                return render_template("carmanage.html", Car=Car, action="")
        except:
            pass

    elif action == "modify":
        try:
            
            #Actual update post request
            if request.method == "POST":
                vin = request.form["vin"]
                make = request.form["make"]
                model = request.form["model"]
                year = request.form["year"]
                retail = request.form["retail"]

                car_exists = Car.query.filter_by(vin=vin).first()
                
                if not car_exists:
                    pass

                #This will eventually have to cascade also
                car_exists.vin = vin
                car_exists.make = make
                car_exists.model = model
                car_exists.year = year
                car_exists.retail = retail
                
                db.session.commit()            
                
                #return to main car management page
                return render_template("carmanage.html", Car=Car, action="", car="")

            #get request to populate post form
            elif request.method == "GET":
                vin = request.args.get("vin")

                car_exists = Car.query.filter_by(vin=vin).first()

                if car_exists:
                    return render_template("carmanage.html", car=car_exists, action=action)
            
        except:
            pass

    #This will eventually have to cascade across all database tables
    elif action == "delete":
           
        vin = request.args.get("vin")

        car_exists = Car.query.filter_by(vin=vin).first()

        if car_exists:
            db.session.delete(car_exists)
            db.session.commit()
        

    return render_template("carmanage.html", action=action, Car=Car)

#Page for viewing and searching for cars in the inventory
@app.route("/carview", methods=['GET'])
def carview():

    #Need to have: Search view
    pass

if __name__ == "__main__":
    app.run()
