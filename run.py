from app import app
import sys

if len(sys.argv) == 1: 
    app.run("127.0.0.1", debug=True)

#This if block will create and initialize the database
#so that the initial admin user with password test is
#present from the very start of the application
#Typically, a user will do: python run.py init
#and then just python run.py to run
if sys.argv[1] == "init":
    from app.db import *
    init_db()
