from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from os import urandom

app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg','jpeg', 'gif', 'bmp', 'tiff'])

app.config['UPLOAD_FOLDER'] = "static/images/"
app.config.from_envvar('FLASKR_SETTINGS', silent = True)

app.secret_key = urandom(24)

#Import views, I changed the directory structure to make it 
#much easier to logically seperate components and over all
#make our project more modular and easier to read rather 
#than retain the one app.py file
from views import *
