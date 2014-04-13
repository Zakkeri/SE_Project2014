#==============================================================================
# File: __init__.py
# Auth: Andrew Calvano / Jim Ching
# Desc: Map classes to DB tables using declarative system.
#
# Changelog
#   * Removed redundant imports.
#==============================================================================
from app.db import db
from app import app

class User(db.Model):
    """Class to represent the Users table.  This table
       contains all user data in the application.     
       UID | Username | Password | IsAdmin"""
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

class Car(db.Model):
    """Class to represent the car inventory layout in the database.
       This will be used for all relations regarding cars
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

class CarPics(db.Model):
    """Class that holds pictures of all cars.
       VIN | PICTURENAME"""
    __tablename__ = "car_pics"
    picname = db.Column(db.String(100), primary_key = True)
    vin = db.Column(db.String(20), db.ForeignKey('car.vin', onupdate="cascade"))

    def __init__(self, vin, picname):
        self.vin = vin
        self.picname = picname

class CustomerInfo(db.Model):
    """Class that holds customer information table.
       CID | Full Name | Addr1 | Addr2 | City | State | Country

       Primary Key consists of cid,fullname, and addr1.  These values
       will be checked upon order creation to see if the customer 
       exists. If not then the customer will be added with new info. If
       they do exist the cid is retrieve and a new order is created in
       the order_info table"""
    __tablename__ = "customer_info"
    cid = db.Column(db.Integer,  unique=True, primary_key=True)
    fname = db.Column(db.String(100))
    addr1 = db.Column(db.String(200))
    addr2 = db.Column(db.String(200))
    city = db.Column(db.String(200))
    state = db.Column(db.String(200))
    pcode = db.Column(db.String(6))
    country = db.Column(db.String(2))
    order_info = db.relationship("OrderInfo", backref="CustomerInfo", cascade="all")

    def __init__(self, cid, fname, addr1, addr2, city, state, pcode, country):
        self.cid = cid
        self.fname = fname
        self.addr1 = addr1
        self.addr2 = addr2
        self.city = city
        self.state = state
        self.pcode = pcode
        self.country = country

class OrderInfo(db.Model):
    """Class that holds a given sale information.
       OID | CID | VIN | Sales Name | Final Price | Status | Delivery Date | Last Updated"""
    __tablename__ = "order_info"
    oid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cid = db.Column(db.Integer, db.ForeignKey("customer_info.cid", onupdate="cascade"), nullable=False)
    vin = db.Column(db.String(20), db.ForeignKey("car.vin", onupdate="cascade"), nullable=False, primary_key=True)
    sname = db.Column(db.String(100))
    fprice = db.Column(db.String(30))
    ddate = db.Column(db.String(20))
    update = db.Column(db.Date)
    status = db.Column(db.String(100))
    delivered = db.Column(db.Boolean)

    def __init__(self, cid, vin, sname, fprice, ddate, update, status="Ready to Process", delivered=False):
        self.cid = cid
        self.vin = vin
        self.sname = sname
        self.fprice = fprice
        self.ddate = ddate
        self.update = update
        self.status = status
        self.delivered = delivered