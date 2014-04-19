#==============================================================================
# File: run.py
# Auth: Andrew Calvano / Jim Ching
# Desc: Start the Flask Application
#==============================================================================
from app import app 				# __init__.py globals
from app.db import init_db    # db.py globals
from sys import argv

if len(argv) >= 2:
	# initialize the admin account
	if argv[1] == 'init':
		init_db()
	else:
		print 'Usage: \'python run.py\' or \'python run.py init\' only.'
else:
	# start the flask application
	app.run('127.0.0.1', debug = True)