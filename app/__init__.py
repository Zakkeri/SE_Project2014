#==============================================================================
# File: __init__.py
# Auth: Andrew Calvano / Jim Ching
# Desc: Create an WSGI application using Flask instance.
# Note: Defines application package for car management application and
#		  initializes all global variables and modules.	
#==============================================================================
from flask import Flask
from os import urandom

#==============================================================================
# Application Globals
#==============================================================================
app = Flask(__name__)
app.config.from_pyfile("app.cfg")
app.secret_key = urandom(24)

# vin table cache into memory
vin_cache = True
vin_tsize = 0
vin_table = []

#==============================================================================
# Import all URL routed functions (modular directory structure)
#==============================================================================
from views.accountviews import *
from views.carviews import *
from views.orderviews import *
from views.serviceviews import *