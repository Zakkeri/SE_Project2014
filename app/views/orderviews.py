#==============================================================================
# File: orderviews.py
# Auth: Andrew Calvano / Jim Ching
# Desc: Order management interface
#==============================================================================
from flask import render_template, request, session, abort, redirect, url_for
from app.dbmodels import CustomerInfo, OrderInfo, Car, db 
from datetime import datetime
from app import app
from app.util import validate_table

# form tables (validation purposes)
orderadd_ft = ['full-name', 'address-line1', 'address-line2', 'city', 'region', 'postal-code', 'country', 'vin', 'sname', 'price', 'ddate']
orderpoc_ft = ['action', 'oid']

@app.route("/orders", methods=['GET'])
@app.route("/orders/<int:page>", methods=['GET'])
def ordermanage(page = 1):
   'Central order management interface; restrict to admin or sales only.'
   # check if user is login and check if role is admin or sales
   if 'role' not in session.keys() or session['role'] not in ['Admin','Sales']: 
      return redirect(url_for("home"))
            
   block = OrderInfo.query.paginate(page, 10, False)        
   return render_template("ordertemps/ordermanage.html", orders = block)    

@app.route("/orderhistory", methods=["GET"])
@app.route("/orderhistory/<int:page>", methods=['GET'])
def orderhistory(page = 1):
   'List of cancel and delivered orders; restrict to admin or sales only.'
   # check if user is login and check if role is admin or sales
   if 'role' not in session.keys() or session['role'] not in ['Admin','Sales']: 
      return redirect(url_for("home"))

   block = OrderInfo.query.paginate(page, 10, False)
   return render_template("ordertemps/orderhistory.html", orders=block)

@app.route("/ordergen", methods=["GET", "POST"])
def ordergen():
   'Add a customer order; restrict to admin or sales only.'
   if 'role' not in session.keys() or session['role'] not in ['Admin','Sales']: 
      return redirect(url_for("home"))

   # user submit a order
   if request.method == 'POST':
      if validate_table(orderadd_ft, request.form):
         fname = request.form[orderadd_ft[0]]
         addr1 = request.form[orderadd_ft[1]]
         addr2 = request.form[orderadd_ft[2]]
         city = request.form[orderadd_ft[3]]
         state = request.form[orderadd_ft[4]]
         zipcode = request.form[orderadd_ft[5]]
         country = request.form[orderadd_ft[6]]
         message = ''

         # check if customer exist
         customer = CustomerInfo.query.filter_by(fname = fname, addr1 = addr1).first() 
         if not customer:
            customer = CustomerInfo(fname, addr1, addr2, city, state, zipcode, country)
            db.session.add(customer) 
            db.session.commit()

         cid = customer.cid
         vin = request.form[orderadd_ft[7]]
         sname = request.form[orderadd_ft[8]]
         price = request.form[orderadd_ft[9]]
         ddate = request.form[orderadd_ft[10]]

         # check if car exist
         car = Car.query.filter_by(vin = vin).first()
         if car: 
            car.avail_purchase = False

            # create a new order
            new_order = OrderInfo(cid, vin, sname, price, ddate, datetime.now()) 
            db.session.add(new_order)
            db.session.commit()
            message = 'Customer order added; review the order management list.'
         else:
            message = 'Customer order failed; car({}) cannot be found.'.format(vin)
         return redirect(url_for("ordermanage", message = message))

   # present the original order generation form
   return render_template("ordertemps/ordergen.html", cars = Car.query)

@app.route("/orderproc", methods=["GET"])
def orderproc():
   'Deliver or cancel a customer order; restrict to admin or sales only.'
   if 'role' not in session.keys() or session['role'] not in ['Admin','Sales']: 
      return redirect(url_for("home"))
   message = ''

   # user submit a order
   if request.method == 'GET':
      if validate_table(orderpoc_ft, request.args):
         action = request.args.get(orderpoc_ft[0])
         oid = request.args.get(orderpoc_ft[1])

         if action in ["deliver", "cancel"]:
            # check if order exist
            order = OrderInfo.query.filter_by(oid = oid).first()
            if order:
               # deliver the order
               if action == "deliver":
                  order.delivered = True
                  order.status = "Delivered"
                  order.update = datetime.now()
                  db.session.commit()
                  message = 'Customer order process delivered; please check order history.'
               elif action == "cancel":
                  # check if car exist
                  car = Car.query.filter_by(vin = order.vin).first()
                  if car:
                     car.avail_purchase = True
                     order.status = "Canceled"
                     order.update = datetime.now()
                     db.session.commit()
                  else:
                     message = 'Customer order process failed; invalid car({}) identification.'.format(order.vin)      
            else:
               message = 'Customer order process failed; invalid order({}) identification.'.format(oid)
         else:
            message = 'Customer order process failed; invalid action({}) on customer order.'.format(action)

   return redirect(url_for("ordermanage", message = message))