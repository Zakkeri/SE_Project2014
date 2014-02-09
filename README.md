<p>Changelog<br/>
============================================================<br/>
1000: Add installation instructions for Windows.	[Jim]<br/>
============================================================<br/>
</p>
[Installation Instructions for Windows]<br/>
! If you need help on the installation, then bring computer to class !<br/>
1. Download the Python 2.7.6 (32-bit): http://www.python.org/download/releases/2.7.6/<br/>
&nbsp;&nbsp;1.1: Press WINDOW KEY<br/>
&nbsp;&nbsp;1.2: Search 'Environment Variables'<br/>
&nbsp;&nbsp;1.3: Append to PATH ;C:\Python27 (; is the separator for directories)<br/>
&nbsp;&nbsp;or where you installed your python<br/>
&nbsp;&nbsp;1.4: Open command prompt and enter 'python' to check<br/>
2. Download / install the pre-built MySQL binaries: http://sourceforge.net/projects/mysql-python/<br/>
3. Download / install the pre-built PyCrypto binaries: http://www.voidspace.org.uk/python/modules.shtml#pycrypto<br/>
4. Download get-pip.py: https://raw.github.com/pypa/pip/master/contrib/get-pip.py<br/>
5. python27 get-pip.py or python get-pip.py<br/>
&nbsp;&nbsp;5.1: Press WINDOW KEY<br/>
&nbsp;&nbsp;5.2: Search 'Environment Variables'<br/>
&nbsp;&nbsp;5.3: Append to PATH ;C:\Python27\Scripts (; is the separator for directories)<br/>
&nbsp;&nbsp;or where you installed your python + \Scripts<br/>
&nbsp;&nbsp;5.4: Open command prompt and enter 'pip' to check<br/>
6. pip install SQLAlchemy<br/>
7. pip install Flask<br/>
8. Download the user-friendly GitHub: http://windows.github.com/<br/>
9. Login and clone: https://github.com/Zakkeri/SE_Project2014<br/>
10. Install MySQL for Windows: http://dev.mysql.com/downloads/mysql/<br/>
&nbsp;&nbsp;10.1: Leave the setting alone unless you know what you're doing.<br/>
&nbsp;&nbsp;10.2: Don't lose your root and password.<br/>
&nbsp;&nbsp;10.3: Open MySQL Workbench 6.0<br/>
&nbsp;&nbsp;10.4: Start MySQL server if you need to<br/>
&nbsp;&nbsp;10.5: Open the script SE_Project2014/dbcreate.sql and run it.<br/>
11. Run the project on python and view on browser<br/>
&nbsp;&nbsp;11.0: Change line 5 of __init__.py in dbmodel 'mysql://root:(YOUR ROOT PASSWORD HERE)@127.0.0.1/cardb'
&nbsp;&nbsp;11.1: Open command prompt<br/>
&nbsp;&nbsp;11.2: 'cd C:/Users/<YOUR HOME>/Documents/GitHub/SE_Project2014'<br/>
&nbsp;&nbsp;11.3: 'python27 app.py' or 'python app.py'<br/>
&nbsp;&nbsp;11.4: Open browser and point to 'localhost:5000'<br/>

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
