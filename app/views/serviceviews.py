#==============================================================================
# File: accountviews.py
# Auth: Andrew Calvano / Jim Ching
# Desc: Service management interface
#==============================================================================
from flask import render_template, request, session, abort, redirect, url_for
from app.dbmodels import ServiceInfo, CustomerInfo, OrderInfo, Car
from app.db import db
from app import app

@app.route("/service", methods=['GET'])
@app.route("/service/<int:page>", methods=['GET'])
def service(page = 1):
   'Central service management interface; restrict to admin or sales only.'
   # check if user is login in, otherwise go to home
   if 'role' in session.keys():
      # check if role is admin or sales, otherwise go to home
      if session['role'] in ['Admin','Sales']:
         service_list = ServiceInfo.query.paginate(page, 10, False)
      else:
         return redirect(url_for("home"))
   else:
      return redirect(url_for("home"))
   return render_template("servicetemps/servicemanage.html", service_list = service_list)

@app.route('/serviceadd', methods = ['GET','POST'])
def serviceadd():
   'Add a service order; restrict to admin or sales only.'
   # check if user is login in, otherwise go to home
   if 'role' in session.keys():
      # check if role is admin or sales, otherwise go to home
      if session['role'] in ['Admin','Sales']:
         # user have submitted a service form
         if request.method == 'POST':
            # check if cid is selected
            if 'cid' in request.form:
               # check if vid is selected
               if 'vin' in request.form:
                  # check if service information is given
                  if 'sdesc' in request.form:
                     if 'scost' in request.form:
                        if 'sdate' in request.form:
                           # create the service
                           cid = request.form['cid']
                           vin = request.form['vin']
                           sdesc = request.form['sdesc']
                           scost = request.form['scost']
                           sdate = request.form['sdate']
                           message = ''

                           # check if car exist
                           car = Car.query.filter_by(vin = vin).first()
                           if car:
                              # check if customer exist
                              cust = CustomerInfo.query.filter_by(cid = cid).first()
                              if cust:
                                 # add service
                                 new_service = ServiceInfo(cid, vin, sdesc, scost, sdate)
                                 db.session.add(new_service)
                                 db.session.commit()
                                 message = 'Customer service order added successfully.'
                              else:
                                 message = 'Customer does not exist, cannot service.'
                           else:
                              message = 'Car does not exist, cannot service.'
                           service_list = ServiceInfo.query.paginate(1, 10, False)
                           return render_template("servicetemps/servicemanage.html", service_list = service_list, message = message)

                  # ask for service information
                  return render_template('servicetemps/serviceadd.html', cid = request.form['cid'], vin = request.form['vin'])
               # ask for the vid
               else:
                  vin_list = db.session.query(OrderInfo.cid, OrderInfo.vin, OrderInfo.delivered).from_statement("SELECT DISTINCT * FROM order_info WHERE order_info.cid = :cid AND order_info.delivered = True").params(cid = request.form['cid']).all()
                  vin_list = set(vin_list)
                  return render_template('servicetemps/serviceadd.html', cid = request.form['cid'], vin_list = vin_list)
            # ask for the cid again
            else:
               cid_list = db.session.query(OrderInfo.cid, OrderInfo.delivered).from_statement("SELECT DISTINCT * FROM order_info WHERE order_info.delivered = True").all()
               cid_list = set(cid_list)
               return render_template('servicetemps/serviceadd.html', cid_list = cid_list)   
         # present user with initial form
         elif request.method == 'GET':
            cid_list = db.session.query(OrderInfo.cid, OrderInfo.delivered).from_statement("SELECT DISTINCT * FROM order_info WHERE order_info.delivered = True").all()
            cid_list = set(cid_list)
            return render_template('servicetemps/serviceadd.html', cid_list = cid_list)
      else:
         return redirect(url_for("home"))
   else:
      return redirect(url_for("home"))

@app.route('/servicechange', methods = ['GET','POST'])
def servicechange():
   'Process a service order; restrict to admin or sales only.'
   # check if user is login in, otherwise go to home
   if 'role' in session.keys():
      # check if role is admin or sales, otherwise go to home
      if session['role'] in ['Admin','Sales']:
         # retrieve sid and process!
         action = request.args.get("action")
         sid = request.args.get("sid")
         if action and sid:
            # process the service
            service = ServiceInfo.query.filter_by(sid = sid).first()
            if service.stats == 1:
               if action == 'completed':
                  message = 'Service completed!'
                  service.stats = 2
               elif action == 'cancel':
                  message = 'Service canceled!'
                  service.stats = 0
               else:
                  message = 'Service denied!'
               db.session.commit()
            else:
               message = 'Service already completed or canceled.'

         service_list = ServiceInfo.query.paginate(1, 10, False)
         return render_template("servicetemps/servicemanage.html", service_list = service_list, message = message)
      else:
         return redirect(url_for("home"))
   else:
      return redirect(url_for("home"))

@app.route('/servicehistory', methods = ['GET','POST'])
def servicehistory(page = 1):
   'View history of orders; restricted to admin or sales only.'
   # check if user is login in, otherwise go to home
   if 'role' in session.keys():
      # check if role is admin or sales, otherwise go to home
      if session['role'] in ['Admin','Sales']:
         service_list = ServiceInfo.query.paginate(page, 10, False)
      else:
         return redirect(url_for("home"))
   else:
      return redirect(url_for("home"))
   return render_template("servicetemps/servicehistory.html", service_list = service_list)