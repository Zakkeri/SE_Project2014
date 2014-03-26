from flask.ext.sqlalchemy import SQLAlchemy
from app import app
from app.util import getsalt, createhash

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:test@127.0.0.1/cardb'

#Create a SQLAlchemy object from our app to be used in the
#database setup code
db = SQLAlchemy(app)

def init_db():
    from app.dbmodels import User

    db.create_all()

    #For creating the inital admin user who will be able
    #to create/modify/delete other users inside of the application
    if User.query.filter_by(uname="admin").first():
        pass
    else:
        salt = getsalt()
        passhash = createhash(salt,"test")
        admin = User("admin", salt, passhash, "Admin", 1)
        db.session.add(admin)
        db.session.commit()


