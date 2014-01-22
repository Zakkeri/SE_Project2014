from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:test@127.0.0.1/cardb'
db = SQLAlchemy(app)

class Users(db.Model):
    """Class to represent the Users table.  This table
       represents acutal users of the application
       
       UID | Username | Password | IsAdmin
    """

    uid = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(45), unique=True)
    isadmin = db.Column(db.Boolean)

    def __init__(self, uid, uname, password):
        self.uid = uid
        self.uname = uname
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.uname

