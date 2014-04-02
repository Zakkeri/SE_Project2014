"""
The carviews module contains all views that are relevant
to the car inventory system.  These do not include views
that are associated with user accounts, orders, or main-
tenance.  

Each function is a seperate route on the webserver with a
one-to-one mapping of page to function with the possiblity
of either a GET or POST request in many situations.
"""

from flask import render_template, request, session, \
                  abort, redirect, url_for
from app.dbmodels import Car, CarPics, CarFeatures
from app.db import db
from app import app

#Page for car management accessible by admins and sales
#Maybe should figure out how to paginate for more than 30 entries in a table
@app.route("/carmanage", methods=['GET'])
@app.route("/carmanage/<int:page>", methods=['GET'])
def carmanage(page = 1):
    """This function's sole purpose is to serve up the management
       table for cars in inventory.
        
       The management interface gives the ability of uploading pictures,
       adding cars, modifying cars, deleting cars, and adding features to
       cars
    """
    
    if "role" not in session:
        abort(401)

    #Only allow Admins and Sales Users for accessing
    if session["role"] not in ["Admin", "Sales"]:
        return redirect(url_for("home"))
    
    #Another cool feature would be to sort by make/model/year/vin/etc
    sort = request.args.get("sort")

    if sort == "vin":
        block = Car.query.order_by("vin desc").paginate(page, 10, False)
    elif sort == "make":
        block = Car.query.order_by("make desc").paginate(page, 10, False)
    elif sort == "model":
        block = Car.query.order_by("model desc").paginate(page, 10, False)
    elif sort == "year":
        block = Car.query.order_by("year desc").paginate(page, 10, False)
    elif sort == "retail":
        block = Car.query.order_by("retail desc").paginate(page, 10, False) 
    else:
        block = Car.query.paginate(page, 10, False)

    return render_template("cartemps/carmanage.html", cars=block)

#Page for adding a car to inventory
@app.route("/caradd", methods=['GET', 'POST'])
def caradd():
    """This function implements the logic for a user
       to be able to add a car to the inventory system.

       Only a Sales or Admin user can do this.

       A form must be filled out that asks for some basic
       information about the car.  There is a post request
       that is processed by this function with the characteristics
       and a new entry is placed in the car inventory table if
       the supplied vin is unique in the table.
    """

    if "role" not in session:
        abort(401)

    #Only allow Admins and Sales Users for accessing
    if session["role"] not in ["Admin", "Sales"]:
        return redirect(url_for("home"))
 
    if request.method == "GET":
        return render_template("cartemps/caradd.html")

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
    
            return redirect(url_for("carmanage", page=1))
    except:
        return redirect(url_for("carmanage", page=1))


#Page for modifying a car in inventory
@app.route("/carmod", methods=['GET', 'POST'])
def carmod():
    """Page logic to modify a car's basic information in the
       inventory.  Will accept a GET or POST request and the 
       template and logic behave differently based on which
       request type it is.

       If a get request, the queried car's information is pre-
       loaded in a form to make it easier for a user to modify
       the information as they will not have to enter in every
       field over again

       Still need to add a check for changing the vin as this
       would probably break stuff
    """

    if "role" not in session:
        abort(401)

    #Only allow Admins and Sales Users for accessing
    if session["role"] not in ["Admin", "Sales"]:
        return redirect(url_for("home"))

    try:
            #Actual update post request
            if request.method == "POST":
                vin = request.form["vin"]
                make = request.form["make"]
                model = request.form["model"]
                year = request.form["year"]
                retail = request.form["retail"]

                car_exists = Car.query.filter_by(vin=vin).first()
               
                #If there is an error in the query return to management page 
                if not car_exists:
                    return redirect(url_for("carmanage", page=1))

                #This will eventually have to cascade also
                #VIN should probably be checked also
                car_exists.vin = vin
                car_exists.make = make
                car_exists.model = model
                car_exists.year = year
                car_exists.retail = retail
                
                db.session.commit()            
                
                #return to main car management page
                return redirect(url_for("carmanage", page=1))

            #get request to populate post form
            elif request.method == "GET":

                vin = request.args.get("vin")

                #If not vin GET argument
                if not vin: redirect(url_for("carmanage"))

                car_exists = Car.query.filter_by(vin=vin).first()

                if car_exists:
                    return render_template("cartemps/carmod.html", car=car_exists)
            
    except:
        pass


#page for deleing a car from inventory
@app.route("/cardel", methods=["GET"])
def cardel():
    """Page logic to delete a car from inventory.
       Need to ensure that this cascades deleting
       inventory info, features info, and pictures
    """

    if "role" not in session:
        abort(401)

    #Only allow Admins and Sales Users for accessing
    if session["role"] not in ["Admin", "Sales"]:
        return redirect(url_for("home"))

    vin = request.args.get("vin")

    if not vin:
        return redirect(url_for("carmanage", page=1))

    car = Car.query.filter_by(vin=vin).first()

    if car:
        db.session.delete(car)
        db.session.commit()

    return redirect(url_for("carmanage",page=1))

#Page for viewing and searching for cars in the inventory
@app.route("/carview", methods=['GET'])
def carview():
    """This function satisfies the requirement for a user
       being able to search for specific cars in inventory
       that have certain features.

       The search algorithm can definitely tweaked a lot better
       as I wrote it rapidly.

       The central idea is for a user to be able to type in words
       into a search bar and retrieve entries in the car inventory 
       system that are most closely related to those words.

       So far, we have cars only that are in inventory and not in 
       maintenance being returned.  Each result is accompanied by a 
       thumbnailed picture and the basic information of the car.
    """ 
    if "role" not in session:
        abort(401)

    #Only allow Admins and Sales Users for accessing
    if session["role"] not in ["Admin", "Sales"]:
        return redirect(url_for("home"))

    #Split supplied keywords from GET request into individual words
    kwds = request.args.get("keywords")


    if not kwds:
        return render_template("cartemps/carview.html")

    #keywords from HTTP Get Request
    kwds = kwds.split(" ") 
    #List of cars to be displayed, in vin form
    vins = []
    
    #Search through relevant tables Car and CarFeatures
    #Terrible O(n^2) search
    #Probably can be heavily modified with little impact, we should just be able to pass car objects to 
    #template and load results that way
    for word in kwds:
        #Search through Car Table
        for car in Car.query.all():
            if word.lower() == car.vin.lower() or word.lower() == car.make.lower() or word.lower() == car.model.lower() or word == car.year.lower() or word.lower() == car.retail.lower():
                if car.vin not in vins:
                    vins.append(car.vin)    
                    
        #Search through CarFeatures Table
        for feat in CarFeatures.query.all():
            if word.lower() in feat.descr.lower() and feat.vin not in vins:
                vins.append(feat.vin)

    #Will need to pass in rows from Car table and CarFeatures to display in template
    #should probably figure out how to paginate this
    return render_template("cartemps/carview.html", Car=Car, CarPics=CarPics, vins=vins, len=len(vins))

@app.route("/addfeatures", methods=['GET', 'POST'])
def addfeatures():
    """This function implements the logic to add features
       which will be attached to a given car in inventory.

       The first step is to check if the car actually exists
       in inventory that matches the vin supplied as a GET
       argument.

       If it does an entry will be made in the CarFeatures
       table for every type of feature that the user chooses
       to fill out for the given car.
    """
   
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
        #Need to implement POST logic for when user supplies
        #features data for a car in POST form

        #If there are no existing car_feats then we will supply to
        #Template anyway cause we have logic in template that expects this
        return render_template('cartemps/addfeature.html', vin=car_exists.vin, feats=feats_dict) 

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

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    """This function implements the necessary operations
       top upload a file for a given car in the inventory
       system
    """

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
      
            return render_template("cartemps/upload.html", car=car_exists)

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
                if not file_exists:
                    new_pic = CarPics(vin=vin, picname=filename) 
                    db.session.add(new_pic)
                    db.session.commit()

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return render_template("cartemps/upload.html", car=car_exists, success=1)

            return render_template("cartemps/upload.html", car=car_exists, success=0)
                
                 
    except Exception, e:
        print e
        return render_template(url_for("home"))
        


