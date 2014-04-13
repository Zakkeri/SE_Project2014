#==============================================================================
# File: carviews.py
# Auth: Andrew Calvano / Jim Ching
# Desc: Car inventory management pages
#
# Changelog
#    * Minor improvements.
#    * Implemented wolf-fence search procedure for carview.
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

# feature criteria table
feat_table = [
    'Performance',
    'Handling',
    'Instrumentation_and_Controls',
    'Safety_and_Security',
    'Exterior_Design',
    'Interior_Design',
    'Audio_System',
    'Comfort_and_Convenience',
    'Maintenance_Programs',
    'Warranties',
    'Extras_Package'
]

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
                    car = Car.query.filter_by(vin = vin).first()
                    if not car:
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
                    car = Car.query.filter_by(vin = vin).first()
                    if car:
                        # modified the car
                        car.vin = new_vin
                        car.make = make
                        car.model = model
                        car.year = year
                        car.retail = retail
                        db.session.add(car)
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
                    return render_template("cartemps/indicarview.html", car=car,feats=feats, pics=pics, panels=panels, extras=extras)
                else:
                    message = 'Invalid VIN and car does not exist.'
            else:
                message = 'Invalid VIN; unable to view car.'
            return redirect(url_for("carmanage", page = 1, message = message))
        else:
            return redirect(url_for("home"))       
    else:
        return redirect(url_for("home"))

@app.route("/addfeatures", methods=['GET', 'POST'])
def addfeatures():
    'Add features to a car in inventory; restrict to admin or sales only.'
   
    # check if user is login in, otherwise go to home
    if 'role' in session.keys():
        # check if role is admin or sales, otherwise go to home
        if session['role'] in ['Admin','Sales']:
            vin = request.args.get("vin")
            message = ''
            if vin:
                car = Car.query.filter_by(vin = vin).first()
                if car:
                    # retrieve all car's features
                    feat_car = CarFeatures.query.filter_by(vin = vin).all()
                    # auto-fill the form
                    if request.method == "GET":
                        feat_dict = {fcar.feat_type:fcar.descr for fcar in feat_car}
                        return render_template('cartemps/addfeature.html', vin = car.vin, feats = feat_dict, feats_list = feat_table) 
                    # user submit features for car
                    if request.method == "POST":
                        # retrieve all entered features
                        feat_list = [request.form[feat] for feat in feat_table]

                        # update car features
                        for ftype, feat in zip(feat_table,feat_list):
                            override = False
                            # check if feature already exist
                            for fcar in feat_car:
                               # override existing feature
                               if ftype == fcar.feat_type:
                                   fcar.descr = feat
                                   override = True
                                   break
                            # check if feature does not exit
                            if not override:
                                feat_new = CarFeatures(car.vin, ftype, feat.strip())
                                db.session.add(feat_new)
                        db.session.commit()

                        return redirect(url_for("addfeatures") + "?vin=" + car.vin)
                else:
                    message = 'Invalid VIN and car does not exist.'
            else:
                message = 'Invalid VIN; unable to add features to car.'
            return redirect(url_for("carmanage", page = 1, message = message))
        else:
            return redirect(url_for("home"))       
    else:
        return redirect(url_for("home"))

@app.route("/carview", methods=['GET', 'POST'])
def carview():
    'Search the car inventory; accessible by everyone.'
    # check if user is login in, otherwise go to home
    if 'role' in session.keys():
        # user initially chooses a make
        if request.method == 'GET':
            # get a list of all unique make
            make_list = db.session.query(Car.make).from_statement("SELECT DISTINCT * FROM car").all()
            # eliminate duplicates
            make_list = set(make_list)
            # render init make list
            return render_template('cartemps/carview.html', make_list = make_list)
        # gradually refine search
        elif request.method == 'POST':
            # check if make is selected
            if 'make' in request.form:
                if 'model' in request.form:
                    if 'year' in request.form:
                        vin_list = db.session.query(Car).from_statement("SELECT DISTINCT * FROM car WHERE car.make = :make AND car.model = :model AND car.year = :year").params(make = request.form['make'], model = request.form['model'], year = request.form['year']).all()
                        return render_template('cartemps/carview.html', make = request.form['make'], model = request.form['model'], year = request.form['year'], vin_list = vin_list)
                    # remake the form to get Year
                    else:
                        year_list = db.session.query(Car.make, Car.model, Car.year).from_statement("SELECT DISTINCT * FROM car WHERE car.make = :make AND car.model = :model").params(make = request.form['make'], model = request.form['model']).all()
                        year_list = set(year_list)
                        return render_template('cartemps/carview.html', make = request.form['make'], model = request.form['model'], year_list = year_list)
                # remake the form to get Model
                else:
                    model_list = db.session.query(Car.make, Car.model).from_statement("SELECT DISTINCT * FROM car WHERE car.make = :make").params(make = request.form['make']).all()
                    model_list = set(model_list)
                    return render_template('cartemps/carview.html', make = request.form['make'], model_list = model_list)
            # remake the form to get Make
            else:
                # get a list of all unique make
                make_list = db.session.query(Car.make).from_statement("SELECT DISTINCT * FROM car").all()
                # eliminate duplicates
                make_list = set(make_list)
                # render init make list
                return render_template('cartemps/carview.html', make_list = make_list)
    else:
        return redirect(url_for("home"))