#==============================================================================
# File: db.py
# Auth: Andrew Calvano / Jim Ching
# Desc: SqlAlchemy DB initialization.
# Note: DB connection string is defined in app.cfg, DB uses Flask-SQLAlchemy
#       to interface, and create tables and initial administrator account.
#==============================================================================
from flask.ext.sqlalchemy import SQLAlchemy
from app import app
from app.util import getsalt, createhash

# global database session
db = SQLAlchemy(app)

def init_db():
    'Initializes the SQL tables using SqlAlchemy\'s declarative system.'
    # import the ORM classes
    from app.dbmodels import User, CarFeatures, Car, CarPics, \
                             CustomerInfo, OrderInfo, ServiceInfo

    # create the SQL tables
    db.create_all()

    # create an administrator account
    if User.query.filter_by(uname="admin").first() == None:
        salt = getsalt()
        passhash = createhash(salt,"Mko0!")
        admin = User("admin", salt, passhash, "Admin", 1)
        db.session.add(admin)
        db.session.commit()