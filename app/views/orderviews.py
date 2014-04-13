#==============================================================================
# File: orderviews.py
# Auth: Andrew Calvano / Jim Ching
# Desc: Order management interface
# Note: create and process orders, remove car from inventory unless cancelled,
#       cancel or delivery will be added to car history table, avail_purchase
#       will be set accordingly.
#
# Changelog
#    * Consistency and removing some logic.
#==============================================================================
from flask import render_template, request, session, abort, redirect, url_for
from app.dbmodels import CustomerInfo, OrderInfo, Car, db 
from datetime import datetime
from app import app

@app.route("/orders", methods=['GET'])
@app.route("/orders/<int:page>", methods=['GET'])
def ordermanage(page = 1):
    'Central order management interface; restrict to admin or sales only.'
    # check if user is login in, otherwise go to home
    if 'role' in session.keys():
        # check if role is admin or sales, otherwise go to home
        if session['role'] in ['Admin','Sales']:
            block = OrderInfo.query.paginate(page, 10, False)        
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

    # return order manage
    return render_template("ordertemps/ordermanage.html", orders = block)    

@app.route("/ordergen", methods=["GET", "POST"])
def ordergen():
    'Add a customer order; restruct to admin or sales only.'
    # check if user is login in, otherwise go to home
    if 'role' in session.keys():
        # check if role is admin or sales, otherwise go to home
        if session['role'] in ['Admin','Sales']:
            # user have submitted a order
            if request.method == "POST":
                # extract customer form data
                message = ''
                fname = request.form["full-name"]
                addr1 = request.form["address-line1"]
                addr2 = request.form["address-line2"]
                city = request.form["city"]
                state = request.form["region"]
                zipcode = request.form["postal-code"]
                country = request.form["country"]

                # check if customer exist
                cust = CustomerInfo.query.filter_by(fname = fname, addr1 = addr1).first() 
                # create new customer if don't exist
                if not cust:
                    cust = CustomerInfo(fname, addr1, addr2, city, state, zipcode, country)
                    db.session.add(cust) 
                    db.session.commit()
                # extract cid
                cid = cust.cid

                # extract sales form data
                vin = request.form["vin"]
                sname = request.form["sname"]
                price = request.form["price"]
                ddate = request.form["ddate"]
                
                # check if car exist
                car = Car.query.filter_by(vin = vin).first()
                if car:
                    # remove car from inventory
                    car.avail_purchase = False

                    # create a new order
                    new_order = OrderInfo(cid, vin, sname, price, ddate, datetime.now()) 
                    db.session.add(new_order)
                    db.session.commit()
                    message = 'Customer order added successfully.'
                else:
                    message = 'Car does not exist.'    
                # return to order management interface
                return redirect(url_for("ordermanage", message = message))
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

    # present the original order generation form
    return render_template("ordertemps/ordergen.html",cars = Car.query)

@app.route("/orderhistory", methods=["GET"])
@app.route("/orderhistory/<int:page>", methods=['GET'])
def orderhistory(page = 1):
    'List of cancel and delivered orders; restrict to admin or sales only.'
    # check if user is login in, otherwise go to home
    if 'role' in session.keys():
        # check if role is admin or sales, otherwise go to home
        if session['role'] in ['Admin','Sales']:
            block = OrderInfo.query.paginate(page, 10, False)
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

    # return order manage
    return render_template("ordertemps/orderhistory.html", orders=block)

@app.route("/orderproc", methods=["GET"])
def orderproc():
    'Deliver or cancel a customer order; restrict to admin or sales only.'
    # check if user is login in, otherwise go to home
    if 'role' in session.keys():
        # check if role is admin or sales, otherwise go to home
        if session['role'] in ['Admin','Sales']:
            # check action exist
            message = ''
            action = request.args.get("action")
            if action and action in ["deliver", "cancel"]:
                # check if order exist
                oid = request.args.get("oid")
                if oid:
                    # check if order exist in DB
                    order = OrderInfo.query.filter_by(oid = oid).first()
                    if order:
                        # deliver the order
                        if action == "deliver":
                            order.status = "Delivered"
                            order.update = datetime.now()
                            db.session.commit()
                            message = 'Customer order successfully delivered.'
                        elif action == "cancel":
                            # check if car exist
                            car = Car.query.filter_by(vin = order.vin).first()
                            if car:
                                car.avail_purchase = True
                                order.status = "Canceled"
                                order.update = datetime.now()
                                db.session.commit()
                            else:
                                message = 'Invalid VIN for order ID on customer order; car does not exist.'
                        else:
                            message = 'Invalid action on customer order.'
                    else:
                        message = 'Invalid order ID on customer order; order does not exist.'
                else:
                    message = 'Invalid order ID on customer order.'
            else:
                message = 'Invalid action on customer order.'

            return redirect(url_for("ordermanage", message = message))
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))