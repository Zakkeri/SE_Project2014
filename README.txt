[Installation Instructions for Windows] 
1. Download the Python 2.7.6 (32-bit): http://www.python.org/download/releases/2.7.6/ 
   1.1: Press WINDOW KEY 
   1.2: Search 'Environment Variables' 
   1.3: Append to PATH ;C:\Python27 (; is the separator for directories) 
   or where you installed your python 
   1.4: Open command prompt and enter 'python' to check 
2. Download / install the pre-built MySQL binaries: http://sourceforge.net/projects/mysql-python/ 
3. Download / install the pre-built PyCrypto binaries: http://www.voidspace.org.uk/python/modules.shtml#pycrypto 
4. Download get-pip.py: https://raw.github.com/pypa/pip/master/contrib/get-pip.py 
5. python27 get-pip.py or python get-pip.py 
   5.1: Press WINDOW KEY 
   5.2: Search 'Environment Variables' 
   5.3: Append to PATH ;C:\Python27\Scripts (; is the separator for directories) 
   or where you installed your python + \Scripts 
   5.4: Open command prompt and enter 'pip' to check 
6. pip install SQLAlchemy 
7. pip install Flask 
8. Download the user-friendly GitHub: http://windows.github.com/ 
9. Login and clone: https://github.com/Zakkeri/SE_Project2014 
10. Install MySQL for Windows: http://dev.mysql.com/downloads/mysql/ 
   10.1: Leave the setting alone unless you know what you're doing. 
   10.2: Don't lose your root and password. 
   10.3: Open MySQL Workbench 6.0 
   10.4: Start MySQL server if you need to 
   10.5: Open the script SE_Project2014/sql/jimdb.sql and run it. 
11. Run the project on python and view on browser 
   11.0: Change line 1 of app.cfg in dbmodel 'mysql://root:(YOUR ROOT PASSWORD HERE)@127.0.0.1/cardb'
   11.1: Open command prompt 
   11.2: 'cd C:/Users/<YOUR HOME>/Documents/GitHub/SE_Project2014' 
   11.3: 'python27 run.py' or 'python run.py' 
   11.4: Open browser and point to '127.0.0.1:5000' 
