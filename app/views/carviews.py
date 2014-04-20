#==============================================================================
# File: carviews.py
# Auth: Andrew Calvano / Jim Ching
# Desc: Car management interface
#==============================================================================
from flask import render_template, request, session, abort, redirect, url_for
from werkzeug.utils import secure_filename
from app.util import validate_table, genvin
from app.dbmodels import Car, CarPics, CarFeatures
from app.db import db
from app import app, vin_cache, vin_tsize, vin_table
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
    'Instrumentation and Controls',
    'Safety and Security',
    'Exterior Design',
    'Interior Design',
    'Audio_System',
    'Comfort and Convenience',
    'Maintenance Programs',
    'Warranties',
    'Extras_Package'
]

# form tables (validation purposes)
caradd_ft = ['vin','make','model','year','retail']
carmod_ft = ['vin']
cardel_ft = ['vin']
carpic_ft = ['vin']
carind_ft = ['vin']
carfea_ft = ['vin']

@app.route("/carmanage", methods=['GET'])
@app.route("/carmanage/<int:page>", methods=['GET'])
def carmanage(page = 1):
    'Central car inventory management interface; restrict to admin or sales only.'
    if 'role' not in session.keys() or session['role'] not in ['Admin','Sales']: 
        return redirect(url_for("home"))

    # sort the table, otherwise display normally
    if 'sort' in request.args and request.args.get('sort') in sort_table.keys():
        block = Car.query.filter_by(avail_purchase = True).order_by(sort_table[request.args.get('sort')]).paginate(page, 10, False)
    else:
        block = Car.query.filter_by(avail_purchase = True).paginate(page, 10, False)
    return render_template("cartemps/carmanage.html", cars = block)

@app.route("/caradd", methods=['GET', 'POST'])
def caradd():
    'Add a car to inventory; restrict to admin or sales only.'
    global vin_cache, vin_tsize, vin_table
    if 'role' not in session.keys() or session['role'] not in ['Admin','Sales']: 
        return redirect(url_for("home"))

    if request.method == 'POST':
        if validate_table(caradd_ft, request.form):
            vin = request.form[caradd_ft[0]]
            make = request.form[caradd_ft[1]]
            model = request.form[caradd_ft[2]]
            year = request.form[caradd_ft[3]]
            retail = request.form[caradd_ft[4]]
            message = ''

            # validate the form
            if len(vin) != 17:             message = 'VIN must be 17 characters long ({})'.format(len(vin))
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

                    if vin_cache == True:
                        vin_table.append(vin)
                        vin_tsize += 1
                    message = 'Car added; review the car management list.'
                else:
                    message = 'Car failed; {} already exist in database.'.format(vin)
            return redirect(url_for("carmanage", page = 1, message = message))
        
    return render_template('cartemps/caradd.html', vin = genvin())

@app.route("/carmod", methods=['GET', 'POST'])
def carmod():
    'Modify a car in inventory; restrict to admin or sales only.'
    if 'role' not in session.keys() or session['role'] not in ['Admin','Sales']: 
        return redirect(url_for("home"))

    # user submitted a modification
    if request.method == "POST":
        if validate_table(caradd_ft, request.form):
            vin = request.form[caradd_ft[0]]
            make = request.form[caradd_ft[1]]
            model = request.form[caradd_ft[2]]
            year = request.form[caradd_ft[3]]
            retail = request.form[caradd_ft[4]]
            message = ''

            # validate the form
            if len(vin) != 17:             message = 'VIN must be 17 characters long ({})'.format(len(vin))
            if not 1 <= len(make) <= 30:   message = 'Make must be 1 to 30 characters long ({})'.format(len(make))
            if not 1 <= len(model) <= 30:  message = 'Model must be 1 to 30 characters long ({})'.format(len(model))
            if len(year) != 4:             message = 'Year must be 4 characters long ({})'.format(len(year))
            if not 1 <= len(model) <= 30:  message = 'Retail price must be 1 to 30 characters long ({})'.format(len(model))

            # check if form is validated
            if message == '':
                car = Car.query.filter_by(vin = vin).first()
                if car:
                    car.make = make
                    car.model = model
                    car.year = year
                    car.retail = retail
                    db.session.add(car)
                    db.session.commit()
                    message = 'Car modified; review the car management list.'
                else:
                    message = 'Car failed to modify; invalid car({}) identification.'.format(vin)

            #return to main car management page
            return redirect(url_for("carmanage", page = 1, message = message))
    # user presented with current car information
    elif request.method == "GET":
        if validate_table(carmod_ft, request.args):
            vin = request.args.get(carmod_ft[0])
            car = Car.query.filter_by(vin = vin).first()
            if car: return render_template("cartemps/carmod.html", car = car)
    return redirect(url_for("home"))

@app.route("/cardel", methods=["GET"])
def cardel():
    'Delete a car in inventory; restrict to admin or sales only.'
    if 'role' not in session.keys() or session['role'] not in ['Admin','Sales']: 
        return redirect(url_for("home"))

    if validate_table(cardel_ft, request.args):
        vin = request.args.get(cardel_ft[0])
        car = Car.query.filter_by(vin = vin).first()
        if car:
            db.session.delete(car)
            db.session.commit()
            return redirect(url_for("carmanage", page = 1, message = 'Car deleted; review the car management list.'))
        else:
            return redirect(url_for("carmanage", page = 1, message = 'Car failed to delete; invalid car({}) identification.'.format(vin)))

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    'Upload a car picture to the server; restrict to admin or sales only.'
    if 'role' not in session.keys() or session['role'] not in ['Admin','Sales']: 
        return redirect(url_for("home"))

    # user want to upload a picture for the car
    if request.method == "GET":
        if validate_table(carpic_ft, request.args):
            vin = request.args.get('vin')
            car = Car.query.filter_by(vin = vin).first()
            if car: return render_template("cartemps/upload.html", car = car)
    # user uploaded a picture for the car
    elif request.method == "POST":
        if validate_table(carpic_ft, request.args):
            vin = request.args.get(carpic_ft[0])
            car = Car.query.filter_by(vin = vin).first()
            if car and 'file' in request.files:
                file = request.files['file']
                if file and file.filename.rsplit('.', 1)[1] in ["jpg", "tiff", "jpeg", "bmp", "gif", "png"]:
                    #check if filename is already in database
                    filename = secure_filename(vin + file.filename)
                    file_exists = CarPics.query.filter_by(vin = vin, picname = filename).first()
                    if not file_exists:
                        new_pic = CarPics(vin = vin, picname = filename)
                        db.session.add(new_pic)
                        db.session.commit()
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        message = 'Upload picture; view car information for picture.'
                    else:
                        message = 'Upload picture failed; file name already exist.'
                else:
                    message = 'Upload picture failed; invalid file or file extension.'
            else:
                message = 'Upload picture failed; invalid car({}) identification.'.format(vin)
        return redirect(url_for("carmanage", page = 1, message = message))
    return redirect(url_for("home"))

@app.route("/indicar", methods=["GET"])
def indicar():
    'Display car information and pictures.'
    message = ''
    if request.method == "GET":
        if validate_table(carind_ft, request.args):
            vin = request.args.get(carind_ft[0])
            car = Car.query.filter_by(vin = vin).first()
            if car:
                feats = CarFeatures.query.filter_by(vin = vin)
                pics = CarPics.query.filter_by(vin = vin)
                panels, extras = divmod(pics.count(), 3)
                return render_template("cartemps/indicarview.html", car = car, feats = feats, pics = pics, panels = panels, extras = extras)
            else:
                message = 'Unable to view car information; invalid car({}) identification.'.format(vin)
    return redirect(url_for("carmanage", page = 1, message = message))

@app.route("/addfeatures", methods=['GET', 'POST'])
def addfeatures():
    'Add features to a car in inventory; restrict to admin or sales only.'
    if 'role' not in session.keys() or session['role'] not in ['Admin','Sales']: 
        return redirect(url_for("home"))

    message = ''
    if validate_table(carfea_ft, request.args):
        vin = request.args.get('vin')
        car = Car.query.filter_by(vin = vin).first()
        if car:
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

                return redirect(url_for("carmanage", page = 1, message = "Feature added; please review the car information."))
        else:
            message = 'Add feature failed; invalid car({}) identification.'.format(vin)
        return redirect(url_for("carmanage", page = 1, message = message))

@app.route("/carview", methods=['GET', 'POST'])
def carview():
    'Search the car inventory; accessible by everyone.'
    # check if user is login in, otherwise go to home
    if 'role' in session.keys():
        # user initially chooses a make
        if request.method == 'GET':
            # search form
            make_list = db.session.query(Car.make).from_statement("SELECT DISTINCT * FROM car").all()
            make_list = set(make_list)
            return render_template('cartemps/carview.html', make_list = make_list, car_list = Car.query.filter_by(avail_purchase = True))
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
                make_list = db.session.query(Car.make).from_statement("SELECT DISTINCT * FROM car").all()
                make_list = set(make_list)
                return render_template('cartemps/carview.html', make_list = make_list)
    else:
        return redirect(url_for("home"))