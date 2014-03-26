'''
This module contains a couple of important objects that are 
critical to the application's database connection.

app is retrieved from the app module and is configure such that
the app will use a specified database url for the SQLAlchemy
connection.

db is the actualy Flask-SQLAlchemy object used for all database
operations throughout the application.

In many of the view files there is code such as:

    db.add(user)
    db.commit()

This is standard syntax for making a change to the current ORM session
and then commiting those changes to the actual database.

The init_db function is used to initialize the application's database:
  
  1.) Create all tables specified in the dbmodels module
  2.) Create a default Administrator level user with credentials
       
        Username: admin
        Password: test
'''


from flask.ext.sqlalchemy import SQLAlchemy
from app import app
from app.util import getsalt, createhash


#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:test@127.0.0.1/testcardb"
db = SQLAlchemy(app)


def init_db():
    '''Function for creating and intializing all ORM models
       from dbmodels package, as well as placing the inital 
       admin user into the database.
    ''' 
    from app.dbmodels import User

    db.create_all()

    #For creating the inital admin user who will be able
    #to create/modify/delete other users inside of the application
    if User.query.filter_by(uname="admin").first():
        pass
    else:
        salt = getsalt()
        passhash = createhash(salt,"test")
        admin = User("admin", salt, passhash, "Admin", 1)
        db.session.add(admin)
        db.session.commit()

