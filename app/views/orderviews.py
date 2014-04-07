'''
All logic for order operations.

ordermanage is an interface for sales and admins to process
sales orders

ordergen is an interface for sale and admins to create new
orders based on cars in inventory. Once the order is created 
the car will be removed in inventory unless the order is 
cancelled. If the order is cancelled the car will be placed
back into inventory as an available car to purchase. If the 
order is delivered the car will be removed as an available
car to purchase.

If an order is cancelled or delivered it will be added to
the car history table and will not be included in the
listings of the carmanage page as its avail_purchase
field will be set to false.
'''

from flask import render_template, request, session, \
                  abort, redirect, url_for
from app.dbmodels import CustomerInfo, OrderInfo, Car, db 
from datetime import datetime
from app import app

global_cid = 1

#When initializing database may have to comment these next to
#lines out as CustomerInfo name is not available yet
if CustomerInfo.query.first():
    global_cid = CustomerInfo.query[::-1][0].cid + 1

@app.route("/orders", methods=['GET'])
@app.route("/orders/<int:page>", methods=['GET'])
def ordermanage(page = 1):
    '''This is the central console for sales/admins
       users to manage orders for cars in inventories.

       It provides an interface listing all current orders
       that have not been cancelled or delivered.

       It provides each user the option to cancel or deliver
       an order.  Each function will move the order into the
       order history table. If an order is cancelled the car
       is marked as available to purchase again.
    '''

    if "role" not in session:
        return redirect(url_for("home"))

    #Only allow Admins and Sales Users for accessing
    if session["role"] not in ["Admin", "Sales"]:
        return redirect(url_for("home"))

    #Pagination code, may add support for sorting
    block = OrderInfo.query.paginate(page, 10, False)

    return render_template("ordertemps/ordermanage.html", 
                            orders=block)

@app.route("/ordergen", methods=["GET", "POST"])
def ordergen():
    '''This page allows a user of sales/admin level

       to create an order and place the order in 
       the system.  

       An order is allowed only if it corresponds to
       an existing car in inventory that is marked as
       available to purchase.

       When the order is placed the car will be marked
       as not available for purchased and will not be 
       listed in the car inventory management page.

       TODO:
       Order cancellation - When the order is cancelled
       the car should be marked as available for purchased
       again.

       Actions - Actions should be Cancel Order and Deliver
                 Order
                 Once either is pressed the order will be 
                 placed in the Order History table for logging
                 purposes.
    '''
    global global_cid

    if "role" not in session:
        return redirect(url_for("home"))

    if session["role"] not in ["Admin", "Sales"]:
        return redirect(url_for("home"))

    #If data is posted to this page
    if request.method == "POST":

        #Attempt to retreive customer data first
        fname = request.form["full-name"]
        addr1 = request.form["address-line1"]
        addr2 = request.form["address-line2"]
        city = request.form["city"]
        state = request.form["region"]
        zipcode = request.form["postal-code"]
        country = request.form["country"]

        #Query to check if new user creation is necessary
        cust = CustomerInfo.query.filter_by(fname=fname,addr1=addr1).first() 
        #If there was no customer with this name in address
        #Go ahead and create the new customer
        #Should validate data before doing this 
        cid = None
        if cust:
            #Next we need to retrieve the information relevant
            #to the actual order and fill in the OrderInfo 
            #table with the associated CID from above
            cid = cust.cid

        if not cust:
            cust = CustomerInfo(global_cid, fname, addr1, addr2, city, state,
                                zipcode, country)
            global_cid += 1
            db.session.add(cust) 
            cid = cust.cid 
            db.session.commit()

        #Next need to retrieve order data
        #Will eventually have to validate this data also 
        vin = request.form["vin"]
        sname = request.form["sname"]
        price = request.form["price"]
        ddate = request.form["ddate"]
        
        #Need to check if vin corresponds to actual vin in the
        #database and if not need to spit error to render_template 
        #Probably should also convert template to user entry for
        #VINs into drop down that lists existing VINs, this will
        #prevent a large number of errors from user input
        car_exists = Car.query.filter_by(vin=vin).first()

        if not car_exists:
            #return render_template("ordertemps/ordergen.html", 
            #                         errror="
            return redirect(url_for("ordergen"))

        #"Remove" car from inventory availablilty
        car_exists.avail_purchase = False

        #Create new order
        new_order = OrderInfo(cid, vin, sname, price, ddate, datetime.now()) 
        db.session.add(new_order)
        db.session.commit()
        
        #Return to ordermanage page
        return redirect(url_for("ordermanage"))

    return render_template("ordertemps/ordergen.html",cars=Car.query)

@app.route("/orderproc", methods=["GET"])
def orderproc():

    if "role" not in session:
        return redirect(url_for("home"))

    if session["role"] not in ["Admin", "Sales"]:
        return redirect(url_for("home"))

    action = request.args.get("action")
    if not action or action not in ["deliver", "cancel"]:
        return redirect(url_for("ordermanage"))
    oid = request.args.get("oid")
    if not oid:
        return redirect(url_for("ordermanage"))

    order = OrderInfo.query.filter_by(oid=oid).first()

    if not order:
        return redirect(url_for("ordermanage"))


    if action == "deliver":
        
        order.status = "Delivered"
        order.update = datetime.now()
        db.session.commit()

    elif action == "cancel":
        #If Cancelled make avail_purchase = True
        #and update time of change as well as
        #change status to Canceled    

        car_exists = Car.query.filter_by(vin=order.vin).first()
        if not car_exists:
            return redirect(url_for("ordermanage"))

        car_exists.avail_purchase = True

        order.status = "Canceled"
        order.update = datetime.now()
        db.session.commit()
        

    return redirect(url_for("ordermanage"))

@app.route("/orderhistory", methods=["GET"])
@app.route("/orderhistory/<int:page>", methods=['GET'])
def orderhistory(page = 1):
    '''Generates a list of past orders.
       These past orders can either be delivered
       or cancelled.
        
       As of now no functionality exists to reinstate
       a cancelled a order.  A new order must be 
       created.
    '''

    if "role" not in session:
        return redirect(url_for("home"))

    if session["role"] not in ["Admin", "Sales"]:
        return redirect(url_for("home"))

    block = OrderInfo.query.paginate(page, 10, False)

    return render_template("ordertemps/orderhistory.html", orders=block)
