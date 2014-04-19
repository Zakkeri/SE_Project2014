#==============================================================================
# File: accountviews.py
# Auth: Andrew Calvano / Jim Ching
# Desc: Service management interface
#==============================================================================
from flask import render_template, request, session, abort, redirect, url_for
from app.dbmodels import ServiceInfo, CustomerInfo, OrderInfo, Car
from app.db import db
from app import app, vin_cache, vin_tsize, vin_table
from app.util import editdistance, validate_table

# form tables (validation purposes)
serviceadd_ft = ['vin', 'cid', 'sdesc', 'scost', 'sdate']
servicechg_ft = ['action', 'sid']

@app.route("/service", methods=['GET'])
@app.route("/service/<int:page>", methods=['GET'])
def service(page = 1):
   'Central service management interface; restrict to admin or sales only.'
   # check if user is login and check if role is admin or sales
   if 'role' not in session.keys() or session['role'] not in ['Admin','Sales']: 
      return redirect(url_for("home"))
   service_list = ServiceInfo.query.paginate(page, 10, False)
   return render_template("servicetemps/servicemanage.html", service_list = service_list)

@app.route('/servicehistory', methods = ['GET'])
@app.route("/servicehistory/<int:page>", methods=['GET'])
def servicehistory(page = 1):
   'View history of orders; restricted to admin or sales only.'
   # check if user is login and check if role is admin or sales
   if 'role' not in session.keys() or session['role'] not in ['Admin','Sales']: 
      return redirect(url_for("home"))
   service_list = ServiceInfo.query.paginate(page, 10, False)
   return render_template("servicetemps/servicehistory.html", service_list = service_list)


@app.route('/serviceadd', methods = ['GET','POST'])
def serviceadd():
   'Add a service order; restrict to admin or sales only.'
   # check if user is login and check if role is admin or sales
   if 'role' not in session.keys() or session['role'] not in ['Admin','Sales']: 
      return redirect(url_for("home"))

   # service add template data
   vin_search = ''
   vin_status = 0
   vin_match = []
   vin_ord = None
   vin_car = None
   vin_cus = None

   # user submit a VIN
   if request.method == 'POST':
      # user supplying the service form
      form_completed = True
      for form_entry in serviceadd_ft:
         if form_entry not in request.form:
            form_completed = False; break
      if form_completed:
         print 'form completed!'
         # extract form entries
         vin = request.form[serviceadd_ft[0]]
         cid = request.form[serviceadd_ft[1]]
         sdesc = request.form[serviceadd_ft[2]]
         scost = request.form[serviceadd_ft[3]]
         sdate = request.form[serviceadd_ft[4]]
         message = ''

         # double check the form
         car = Car.query.filter_by(vin = vin).first()
         if car:
            customer = CustomerInfo.query.filter_by(cid = cid).first()
            if customer:
               new_service = ServiceInfo(cid, vin, sdesc, scost, sdate)
               db.session.add(new_service)
               db.session.commit()
               message = 'Customer service order added; review the car management list.'
            else:
               message = 'Customer service order failed; customer({}) cannot be found.'.format(cid)
         else:
            message = 'Customer service order failed; car({}) cannot be found.'.format(vin)
         service_list = ServiceInfo.query.paginate(1, 10, False)
         return render_template("servicetemps/servicemanage.html", service_list = service_list, message = message)

      # user supplying the vin (searching)
      if vin_cache == True and 'vin' in request.form:
         vin_search = request.form['vin']
         if 16 <= len(vin_search) <= 18:
            # check if vin is in vin table
            if vin_search in vin_table:
               vin_car = Car.query.filter_by(vin = vin_search).first()                                 # check if car exist
               if vin_car != None: vin_ord = OrderInfo.query.filter_by(vin = vin_search).first()       # check if car solded
               if vin_ord != None: vin_cus = CustomerInfo.query.filter_by(cid = vin_ord.cid).first()   # check if customer exist
               if vin_cus != None: vin_status = 1
            # check possible matches
            else:
               for vin in vin_table:
                  if editdistance(vin, vin_search) <= 2:
                     vin_match.append(vin)
                     if len(vin_match) > 5: break
               if len(vin_match): vin_status = 2

      return render_template('servicetemps/serviceadd.html', info = [vin_search, vin_status, vin_match, vin_ord, vin_cus, vin_car])

   # display initial user form
   return render_template('servicetemps/serviceadd.html')

@app.route('/servicechange', methods = ['GET','POST'])
def servicechange():
   'Process a service order; restrict to admin or sales only.'
   # check if user is login and check if role is admin or sales
   if 'role' not in session.keys() or session['role'] not in ['Admin','Sales']: 
      return redirect(url_for("home"))
   
   # user attempt to process customer service
   if request.method == 'GET':
      if validate_table(servicechg_ft, request.args):
         # extract form entries
         action = request.args.get(servicechg_ft[0])
         sid = request.args.get(servicechg_ft[1])

         # double check form
         service = ServiceInfo.query.filter_by(sid = sid).first()
         if service:
            if service.stats == 1:
               if action == 'completed':
                  message = 'Customer service completed!'
                  service.stats = 2
               elif action == 'cancel':
                  message = 'Customer service canceled!'
                  service.stats = 0
               else:
                  message = 'Customer service action denied; invalid service process action.'
               db.session.commit()
         else:
            message = 'Customer service action denied; invalid service identification.'
   else:
      message = 'Customer service action denied; invalid form method.'

   service_list = ServiceInfo.query.paginate(1, 10, False)
   return render_template("servicetemps/servicemanage.html", service_list = service_list, message = message)