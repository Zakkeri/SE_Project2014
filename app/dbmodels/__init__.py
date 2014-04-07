from sqlalchemy import Column, Integer, String,\
Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.db import db
from app import app

class User(db.Model):
    """Class to represent the Users table.  This table
       contains all user data in the application.

       Table name will be "user"       
       
       UID | Username | Password | IsAdmin
    """
    __tablename__ = "user"

    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uname = db.Column(db.String(45), unique=True)
    salt = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128), unique=False)
    role = db.Column(db.String(45))
    isadmin = db.Column(db.Boolean)

    def __init__(self, uname, salt, password, role, isadmin):
        self.uname = uname
        self.salt = salt
        self.password = password
        self.role = role
        self.isadmin = isadmin

    def __repr__(self):
        return '<User %r>' % self.uname

class CarFeatures(db.Model):
    """Class that holds performance data for a car if available.

       VIN | feat_type | Description"""

    __tablename__ = "car_features"

    vin = db.Column(db.String(20), db.ForeignKey('car.vin', onupdate="cascade"), primary_key=True)
    feat_type = db.Column(db.String(40), primary_key=True)

    descr = db.Column(db.String(1000))

    def __init__(self, vin, feat_type, descr):

        self.vin = vin
        self.feat_type = feat_type
        self.descr = descr

    def __repr__(self):
        return '<Car %r>' % self.vin


class Car(db.Model):
    """Class to represent the car inventory layout in the database.
       This will be used for all relations regarding cars

       Table name will be "car"
        
        VIN | MAKE | MODEL | YEAR | RETAIL"""

    __tablename__ = "car"

    vin = db.Column(db.String(20), primary_key=True, unique=True)#, onupdate="cascade")
    make = db.Column(db.String(30))
    model = db.Column(db.String(30))
    year = db.Column(db.String(4))
    retail = db.Column(db.String(30))
    avail_purchase = db.Column(db.Boolean)

    features = db.relationship("CarFeatures", backref="Car", cascade="all")
    pics = db.relationship("CarPics", backref="Car", cascade="all")
    order_info = db.relationship("OrderInfo", backref="Car", cascade="all")
    
    def __init__(self, vin, make, model, year, retail,avail_purchase=True):
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.retail = retail 
        self.avail_purchase = avail_purchase

    def __repr__(self):
        return '<Car %r>' % self.vin

class CarPics(db.Model):
    """Class that holds pictures of all cars.
       
        VIN | PICTURENAME
    """

    __tablename__ = "car_pics"

    vin = db.Column(db.String(20), db.ForeignKey('car.vin', onupdate="cascade"))
    picname = db.Column(String(500), primary_key=True, unique=True)

    def __init__(self, vin, picname):
        self.vin = vin
        self.picname = picname

    def __repr__ (self):
        return '<CarPic %r>' % self.picname 

class CustomerInfo(db.Model):
    """Class that holds customer information table.

        CID | Full Name | Addr1 | Addr2 | City | State | Country

       Primary Key consists of cid,fullname, and addr1.  These values
       will be checked upon order creation to see if the customer 
       exists. If not then the customer will be added with new info. If
       they do exist the cid is retrieve and a new order is created in
       the order_info table
    """
    __tablename__ = "customer_info"

    _autoinchack = 0

    cid = db.Column(db.Integer, unique=True, primary_key=True, onupdate="cascade")
    fname = db.Column(db.String(100))
    addr1 = db.Column(db.String(200))
    addr2 = db.Column(db.String(200))
    city = db.Column(db.String(200))
    state = db.Column(db.String(200))
    pcode = db.Column(db.String(6))
    country = db.Column(db.String(2))

    def __init__(self, fname, addr1, addr2, city, state, pcode, country):

        self.cid = self._autoinchack
        self.fname = fname
        self.addr1 = addr1
        self.addr2 = addr2
        self.city = city
        self.state = state
        self.pcode = pcode
        self.country = country

        self._autoinchack += 1

    def __repr__(self):
        return '<CustomerInfo %r>' % self.cid

    order_info = db.relationship("OrderInfo", backref="CustomerInfo", cascade="all")

class OrderInfo(db.Model):
    """Class that hold a given sale information.
        
       OID | CID | VIN | Sales Name | Final Price | Delivery Date | Last Updated
    """
    __tablename__ = "order_info"

    oid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey("customer_info.cid", onupdate="cascade"), nullable=False)
    vin = db.Column(db.String(20), db.ForeignKey("car.vin"), nullable=False, primary_key=True)
    sname = db.Column(db.String(100))
    fprice = db.Column(db.String(30))
    ddate = db.Column(db.String(20))
    update = db.Column(db.Date)

    def __init__(self, cid, vin, sname, fprice, ddate, update):
        self.cid = cid
        self.vin = vin
        self.sname = sname
        self.fprice = fprice
        self.ddate = ddate
        self.update = update

    def __repr__(self):
        return '<OrderInfo %r>' % self.oid
