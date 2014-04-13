#==============================================================================
# File: carviews.py
# Auth: Andrew Calvano / Jim Ching
# Desc: Car inventory management pages
#
# Changelog
#==============================================================================
from flask import render_template, request, session, abort, redirect, url_for
from werkzeug.utils import secure_filename
from app.dbmodels import Car, CarPics, CarFeatures
from app.db import db
from app import app
import os

# sorting criteria table
sort_table = {
    'vin' : 'vin desc',
    'make' : 'make desc',
    'model' : 'model desc',
    'year' : 'year desc',
    'retail' : 'retail desc'
}

@app.route("/carmanage", methods=['GET'])
@app.route("/carmanage/<int:page>", methods=['GET'])
def carmanage(page = 1):
    'Central car inventory management interface; restrict to admin or sales only.'
    # check if user is login in, otherwise go to home
    if 'role' in session.keys():
        # check if role is admin or sales, otherwise go to home
        if session['role'] in ['Admin','Sales']:
            # sort the table, otherwise display normally
            sort = request.args.get('sort')
            if sort in sort_table.keys():
                block = Car.query.order_by(sort_table[sort]).paginate(page, 10, False)
            else:
                block = Car.query.paginate(page, 10, False)
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

    # display the table initially; block will be init otherwise go home
    return render_template("cartemps/carmanage.html", cars = block)

@app.route("/caradd", methods=['GET', 'POST'])
def caradd():
    'Add a car to inventory; restrict to admin or sales only.'
    # check if user is login in, otherwise go to home
    if 'role' in session.keys():
        # check if role is admin or sales, otherwise go to home
        if session['role'] in ['Admin','Sales']:
            # user request to add car
            if request.method == "POST":
                message = ''
                vin = request.form["vin"]
                make = request.form["make"]
                model = request.form["model"]
                year = request.form["year"]
                retail = request.form["retail"] 

                # validate the form
                if len(vin) != 20:             message = 'VIN must be 20 characters long ({})'.format(len(vin))
                if not 1 <= len(make) <= 30:   message = 'Make must be 1 to 30 characters long ({})'.format(len(make))
                if not 1 <= len(model) <= 30:  message = 'Model must be 1 to 30 characters long ({})'.format(len(model))
                if len(year) != 4:             message = 'Year must be 4 characters long ({})'.format(len(year))
                if not 1 <= len(model) <= 30:  message = 'Retail price must be 1 to 30 characters long ({})'.format(len(model))

                # check if form is validated
                if message == '':
                    # check if car already exist
                    car_exists = Car.query.filter_by(vin = vin).first()
                    if not car_exists:
                        # add the car
                        newcar = Car(vin, make, model, year, retail) 
                        db.session.add(newcar)
                        db.session.commit()
                        message = 'Car has been successfully added to the database.'
                    else:
                        message = 'Car has already existed in the database.'
                return redirect(url_for("carmanage", page = 1, message = message))
        else:
            return redirect(url_for("home"))       
    else:
        return redirect(url_for("home"))

    # present car adding form
    return render_template('cartemps/caradd.html')

#Page for modifying a car in inventory
@app.route("/carmod", methods=['GET', 'POST'])
def carmod():
    'Modify a car in inventory; restrict to admin or sales only.'
    # check if user is login in, otherwise go to home
    if 'role' in session.keys():
        # check if role is admin or sales, otherwise go to home
        if session['role'] in ['Admin','Sales']:
            # user submitted a modification
            if request.method == "POST":
                message = ''
                vin = request.args.get("vin")
                new_vin = request.form["vin"]
                make = request.form["make"]
                model = request.form["model"]
                year = request.form["year"]
                retail = request.form["retail"]

                # validate the form
                if len(new_vin) != 20:         message = 'VIN must be 20 characters long ({})'.format(len(new_vin))
                if not 1 <= len(make) <= 30:   message = 'Make must be 1 to 30 characters long ({})'.format(len(make))
                if not 1 <= len(model) <= 30:  message = 'Model must be 1 to 30 characters long ({})'.format(len(model))
                if len(year) != 4:             message = 'Year must be 4 characters long ({})'.format(len(year))
                if not 1 <= len(model) <= 30:  message = 'Retail price must be 1 to 30 characters long ({})'.format(len(model))

                # check if form is validated
                if message == '':
                    # check if car exist
                    car_exists = Car.query.filter_by(vin = vin).first()
                    if car_exists:
                        # modified the car
                        car_exists.vin = new_vin
                        car_exists.make = make
                        car_exists.model = model
                        car_exists.year = year
                        car_exists.retail = retail
                        db.session.add(car_exists)
                        db.session.commit()
                        message = 'Car has been successfully modified.'
                    else:
                        message = 'Car does not exist. ({})'.format(vin)
                
                #return to main car management page
                return redirect(url_for("carmanage", page = 1, message = message))

            # user presented with current car information
            elif request.method == "GET":
                # check if vin exist
                vin = request.args.get("vin")
                if vin:
                    # check if car exist
                    car = Car.query.filter_by(vin = vin).first()
                    if car:
                        return render_template("cartemps/carmod.html", car = car)
                return redirect(url_for("carmanage", page = 1, message = 'Invalid VIN, cannot find automobile.'))
            else:
                return redirect(url_for("home"))
        else:
            return redirect(url_for("home"))       
    else:
        return redirect(url_for("home"))

    # home is the best place to be
    return redirect(url_for("home"))

#page for deleing a car from inventory
@app.route("/cardel", methods=["GET"])
def cardel():
    'Delete a car in inventory; restrict to admin or sales only.'
    # check if user is login in, otherwise go to home
    if 'role' in session.keys():
        # check if role is admin or sales, otherwise go to home
        if session['role'] in ['Admin','Sales']:
            # check if vin exist
                vin = request.args.get("vin")
                if vin:
                    car = Car.query.filter_by(vin = vin).first()
                    if car:
                        # delete the car
                        db.session.delete(car)
                        db.session.commit()
                        return redirect(url_for("carmanage", page = 1, message = 'Car has been successfully deleted.'))
                else:
                    return redirect(url_for("carmanage", page = 1, message = 'Invalid VIN, cannot find automobile.'))
        else:
            return redirect(url_for("home"))       
    else:
        return redirect(url_for("home"))

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    'Upload a car picture to the server; restrict to admin or sales only.'
    # check if user is login in, otherwise go to home
    if 'role' in session.keys():
        # check if role is admin or sales, otherwise go to home
        if session['role'] in ['Admin','Sales']:
            # user want to upload a picture for the car
            if request.method == "GET":
                vin = request.args.get("vin")
                if vin:
                    car = Car.query.filter_by(vin = vin).first()
                    if car:
                        return render_template("cartemps/upload.html", car = car)
                # if the vin failed to match, then show error
                return redirect(url_for("carmanage", page = 1, message = 'Invalid VIN, cannot find automobile.'))  
            # user uploaded a picture for the car
            elif request.method == "POST":
                vin = request.args.get("vin")
                message = ''

                if vin:
                    car = Car.query.filter_by(vin = vin).first()
                    if car:
                        # retrieve the picture
                        file = request.files['file']

                        # check the file extension
                        if file and file.filename.rsplit('.', 1)[1] in ["jpg", "tiff", "jpeg", "bmp", "gif"]:
                            #check if filename is already in database
                            filename = secure_filename(vin + file.filename)
                            file_exists = CarPics.query.filter_by(vin = vin, picname = filename).first()
                            if not file_exists:
                                # add picture
                                new_pic = CarPics(vin = vin, picname = filename)
                                db.session.add(new_pic)
                                db.session.commit()

                                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                                return redirect(url_for("carmanage", page = 1, message = 'Picture uploaded to server successfully.'))
                            else:
                                message = 'Picture already exist for car.'
                        else:
                            message = 'Invalid picture extension not supported; unable to upload picture.'
                    else:
                        message = 'Invalid VIN and car does not exist; unable to upload picture.'
                else:
                    message = 'Invalid VIN; unable to upload picture.'
                return redirect(url_for("carmanage", page = 1, message = message))
        else:
            return redirect(url_for("home"))       
    else:
        return redirect(url_for("home"))

@app.route("/indicar", methods=["GET"])
def indicar():
    'Display car information and pictures; restrict to admin or sales only.'
    # check if user is login in, otherwise go to home
    if 'role' in session.keys():
        # check if role is admin or sales, otherwise go to home
        if session['role'] in ['Admin','Sales']:
            vin = request.args.get("vin")
            message = ''
            if vin:
                car = Car.query.filter_by(vin = vin).first()
                if car:
                    # retrieve all the features
                    feats = CarFeatures.query.filter_by(vin = vin)
                    # retrieve all the pictures
                    pics = CarPics.query.filter_by(vin = vin)
                    # display only three pictures at a time
                    panels, extras = divmod(pics.count(), 3)
                    # render the HTML
                    return render_template("cartemps/indicarview.html", car=car,feats=feats, 
                                            pics=pics, panels=panels, extras=extras)
                else:
                    message = 'Invalid VIN and car does not exist.'
            else:
                message = 'Invalid VIN; unable to view car.'
            return redirect(url_for("carmanage", page = 1, message = message))
        else:
            return redirect(url_for("home"))       
    else:
        return redirect(url_for("home"))

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
    '''for word in kwds:
        #Search through Car Table
        for car in Car.query.all():
            if word.lower() == car.vin.lower() or word.lower() == car.make.lower() or word.lower() == car.model.lower() or word == car.year.lower() or word.lower() == car.retail.lower():
                if car.vin not in vins:
                    vins.append(car.vin)    
             
        #Search through CarFeatures Table
        for feat in CarFeatures.query.all():
            if word.lower() in feat.descr.lower() and feat.vin not in vins:
                vins.append(feat.vin)'''

    #Will need to pass in rows from Car table and CarFeatures to display in template
    #should probably figure out how to paginate this
    #return render_template("cartemps/carview.html", Car=Car, CarPics=CarPics, vins=vins, len=len(vins))
    pass

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
            perf = request.form["Performance"].encode('utf-8')
            hand = request.form["Handling"].encode('utf-8')
            instr = request.form["Instrument"].encode('utf-8')
            safety = request.form["Safety"].encode('utf-8')
            ext = request.form["Extdesign"].encode('utf-8')
            intd = request.form["Intdesign"].encode('utf-8')
            audio = request.form["Audio"].encode('utf-8')   
            comfort = request.form["Comfort"].encode('utf-8')
            maint = request.form["Maintenance"].encode('utf-8')
            warr = request.form["Warranties"].encode('utf-8')
            extra = request.form["Extras"].encode('utf-8') 

            #Saves us some lines of code by allowing us to use a for loop in the following block of code
            feats = [perf, hand, instr, safety, ext, intd, audio, comfort, maint, warr, extra]
            names = ["Performance", "Handling", "Instrument", "Safety", "Extdesign", "Intdesign", 
                     "Audio", "Comfort", "Maintenance", "Warranties", "Extras"]


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