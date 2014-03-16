import sys
import binascii
import os
from flask import Flask, request, session, url_for, \
    abort, render_template, flash, redirect, Response
from werkzeug.utils import secure_filename
from utilities import *
from dbmodels import * #Importing db interface from sqlalchemy

app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', '.bmp', '.tiff'])

app.config['UPLOAD_FOLDER'] = "images/"
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
    car_feats_list = CarFeatures.query.filter_by(vin=vin).all()

    #Get logic to display values for features fields if they
    #already exist
    if request.method == "GET":
        #Constructs a dictionary of available features that can be loaded
        #into view by template using something like feats_dict['performance']
        feats_dict = {feat.feat_type:feat.descr for feat in car_feats_list}
        print feats_dict 
        #Need to implement POST logic for when user supplies
        #features data for a car in POST form

        #If there are no existing car_feats then we will supply to
        #Template anyway cause we have logic in template that expects this
        return render_template('addfeature.html', vin=car_exists.vin, feats=feats_dict) 

    #Actually recieve the message from the web view and process accordingly updating or 
    #creating entries in the CarFeatures table
    if request.method == "POST":

        #Try to recieve values from POST request if there is an issue
        #this will redirect to the application home page
        #Random idea: add alerts to home page for things like
        #service deadlines and delivery dates
        try:
            #Retreive all potential features forms from POST
            #request, if any are blank simply ignore them
            perf = request.form["performance"].encode('utf-8')
            hand = request.form["handling"].encode('utf-8')
            instr = request.form["instrument"].encode('utf-8')
            safety = request.form["safety"].encode('utf-8')
            ext = request.form["extdesign"].encode('utf-8')
            intd = request.form["intdesign"].encode('utf-8')
            audio = request.form["audio"].encode('utf-8')   
            comfort = request.form["comfort"].encode('utf-8')
            maint = request.form["maintenance"].encode('utf-8')
            warr = request.form["warranties"].encode('utf-8')
            extra = request.form["extras"].encode('utf-8') 

            #Saves us some lines of code by allowing us to use a for loop in the following block of code
            feats = [perf, hand, instr, safety, ext, intd, audio, comfort, maint, warr, extra]
            names = ["performance", "handling", "instrument", "safety", "extdesign", "intdesign", 
                     "audio", "comfort", "maintenance", "warranties", "extras"]


            #Hack to retrieve feature types from feature objects
            feats_list = [x.feat_type for x in car_feats_list]

            #This loop will loop through all features in POST request and create/modify objects
            #and update the db session
            for index in range(len(feats)):
               
                #If the value from post request is not empty and there is an existing entry
                #for the car with the specific feature type from POST request, modify the 
                #entry in the database 
                if feats[index].strip() != "" and names[index] in feats_list:#car_feats_list.filter_by(feat_type=names[index]):
                    #ugly hack to cycle through rows in query to find correct one to modify
                    for x in car_feats_list:
                        if x.feat_type == names[index]:
                            x.descr = feats[index].strip()

                elif feats[index].strip() != "" and names[index] not in feats_list:
                    newrow = CarFeatures(car_exists.vin, names[index], feats[index].strip())
                    db.session.add(newrow)


            db.session.commit()

            return redirect(url_for("addfeatures") + "?vin=" + car_exists.vin)
 

        #On any type of error redirect to the home page
        except Exception, e:
            print e
            return redirect(url_for("home"))

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

@app.route("/upload", methods=['GET', 'POST'])
def upload():

    if "role" not in session:
        abort(401)

    #Only allow Admins and Sales Users for accessing
    if session["role"] not in ["Admin", "Sales"]:
        return redirect(url_for("home"))


    try:
       #if GET request 
       if request.method == "GET":
            vin = request.args.get("vin")

            car_exists = Car.query.filter_by(vin=vin).first() 

            if not car_exists:
                return redirect(url_for("home"))
      
            return render_template("upload.html", car=car_exists)

       if request.method == "POST":

            vin = request.args.get("vin")

            car_exists = Car.query.filter_by(vin=vin).first()

            if not car_exists:
                return redirect(url_for("home"))

            file = request.files['file']
            if file and file.filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
                filename = secure_filename(vin + file.filename)

                #check if filename is already in database
                file_exists = CarPics.query.filter_by(vin=vin,picname=filename).first()
                print file_exists 
                if not file_exists:
                    new_pic = CarPics(vin=vin, picname=filename) 
                    db.session.add(new_pic)
                    db.session.commit()

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return render_template("upload.html", car=car_exists, success=1)

            return render_template("upload.html", car=car_exists, success=0)
                
                 
    except Exception, e:
        print e
        return render_template(url_for("home"))
        


#Page for viewing and searching for cars in the inventory
@app.route("/carview", methods=['GET'])
def carview():
    
    if "role" not in session:
        abort(401)

    #Only allow Admins and Sales Users for accessing
    if session["role"] not in ["Admin", "Sales"]:
        return redirect(url_for("home"))

    #Split supplied keywords from GET request into individual words
    kwds = request.args.get("keywords")


    if not kwds:
        return render_template("carview.html")

    #keywords from HTTP Get Request
    kwds = kwds.split(" ") 
    #List of cars to be displayed, in vin form
    cars = []
    #Search through relevant tables Car and CarFeatures
    #Terrible O(n^2) search

    for word in kwds:
        #Search through Car Table
        for car in Car.query.all():
            if word.lower() == car.vin.lower() or word.lower() == car.make.lower() or word.lower() == car.model.lower() or word == car.year.lower() or word.lower() == car.retail.lower():
                cars.append(car.vin)     
                    
        #Search through CarFeatures Table
        for feat in CarFeatures.query.all():
            if word in feat.descr and feat.vin not in cars:
                cars.append(car.vin)

    #Will need to pass in rows from Car table and CarFeatures to display in template
    return render_template("carview.html")

if __name__ == "__main__":
    app.run()
