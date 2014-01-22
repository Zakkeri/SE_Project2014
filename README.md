A Car Inventory Management System implemented in python.

----Dependency Installation----

On Ubuntu 12.04

sudo apt-get install python-pip python-flask

sudo pip install flask-sqlalchemy

----Database Configuration----

sudo apt-get install mysql-server

When prompted for information, type in user info.

To setup;

mysql -u username -p

Enter your password.

Run:

source dbcreate.sql;

This will create the database called cardb that will be manipulated by sqlalchemy.
