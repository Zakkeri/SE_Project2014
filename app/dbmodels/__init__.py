from sqlalchemy import Column, Integer, String,\
Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.db import db

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
     
'''
class CarFeatures(db_base):
    """Class that holds performance data for a car if available.

       VIN | feat_type | Description"""

    __tablename__ = "car_features"

    vin = Column(String(20), ForeignKey('car.vin'), primary_key=True)
    feat_type = Column(String(40), primary_key=True)

    descr = Column(String(1000))

    def __init__(self, vin, feat_type, descr):

        self.vin = vin
        self.feat_type = feat_type
        self.descr = descr

    def __repr__(self):
        return '<Car %r>' % self.vin


class Car(db_base):
    """Class to represent the car inventory layout in the database.
       This will be used for all relations regarding cars

       Table name will be "car"
        
        VIN | MAKE | MODEL | YEAR | RETAIL"""

    __tablename__ = "car"

    vin = Column(String(20), primary_key=True, unique=True)
    make = Column(String(30))
    model = Column(String(30))
    year = Column(String(4))
    retail = Column(String(10))

    features = relationship("CarFeatures", backref="Car", cascade="all,delete")
    
    def __init__(self, vin, make, model, year, retail):
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.retail = retail 

    def __repr__(self):
        return '<Car %r>' % self.vin

class CarPics(db_base):
    """Class that holds pictures of all cars.
       
        VIN | PICTURENAME
    """

    __tablename__ = "car_pics"

    vin = Column(String(20), ForeignKey('car.vin'))
    picname = Column(String(500), primary_key=True, unique=True)

    def __init__(self, vin, picname):
        self.vin = vin
        self.picname = picname

    def __repr__ (self):
        return '<CarPic %r>' % self.picname 
'''
