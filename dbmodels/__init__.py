from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:test@127.0.0.1/cardb'
db = SQLAlchemy(app)

class User(db.Model):
    """Class to represent the Users table.  This table
       represents acutal users of the application
       
       UID | Username | Password | IsAdmin
    """

    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uname = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(45), unique=True)
    isadmin = db.Column(db.Boolean)

    def __init__(self, uname, password, isadmin):
        self.uname = uname
        self.password = password
        self.isadmin = isadmin

    def __repr__(self):
        return '<User %r>' % self.uname

