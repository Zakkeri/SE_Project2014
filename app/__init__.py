"""
The app package contains all code to run the car management
application.

This intialization file creates the actual app object and
loads/registers views to the app.

The actual application is run in the parent directory's run.py
file.

Configuration options are placed in the "app.cfg" file
"""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from os import urandom

app = Flask(__name__)
app.debug = True
app.config.from_pyfile("app.cfg")


app.secret_key = urandom(24)

#Import views, I changed the directory structure to make it 
#much easier to logically seperate components and over all
#make our project more modular and easier to read rather 
#than retain the one app.py file
from views.accountviews import *
from views.carviews import *
from views.orderviews import *
