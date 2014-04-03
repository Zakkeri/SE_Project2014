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
from app import app

@app.route("/orders")
def ordermanage():

    if "role" not in session:
        return redirect(url_for("home"))

    #Only allow Admins and Sales Users for accessing
    if session["role"] not in ["Admin", "Sales"]:
        return redirect(url_for("home"))

    return render_template("ordertemps/ordermanage.html")

@app.route("/ordergen")
def ordergen():

    if "role" not in session:
        return redirect(url_for("home"))

    if session["role"] not in ["Admin", "Sales"]:
        return redirect(url_for("home"))

    return render_template("ordertemps/ordergen.html")
