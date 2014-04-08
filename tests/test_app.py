#Unit test file for the Car Inventory Management System Application
import unittest
from flask.ext.testing import TestCase
from os import urandom
from random import seed, randint
from app import app
from app.util import getsalt, createhash
from app.dbmodels import User
from app.db import db

#Used to make tests more random
seed = urandom(1024)

class MyTest(TestCase):

    Testing = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_user(self, username, password, perm_level):

        salt = getsalt()
        passhash = createhash(salt,password)

        if perm_level == "Admin":
            db.session.add(User(username, salt, passhash, perm_level, 1))
        else:
            db.session.add(User(username, salt, passhash, perm_level, 0))
        db.session.commit()

class AccountsUnitTesting(MyTest):
    
    def test_login(self):
        """Unit test for login functionality
        """
        
        #First create two different users in the
        #user table that will be guest and sales
        #permission levels. Admin is there by default.
        self.create_user("admin", "test", "Admin")
        self.create_user("Sales1", "Test1", "Sales")
        self.create_user("Guest1", "Test2", "Guest")
        
        #Try login in as default admin
        response = self.client.post("/login", data=dict(username="admin", password="test"), follow_redirects=True)
        assert "Welcome" in response.data

        #Try accessing login page while logged in as admin
        response = self.client.get("/login", follow_redirects=True) 
        assert "username" not in response.data

        response = self.client.post("/login", data=dict(username="test", password="test"), follow_redirects=True)
        assert response.status != "200 OK"
        
        #logout as admin 
        response = self.client.get("/logout", follow_redirects=True)
        assert "Welcome" not in response.data
        
        #Try login as admin with incorrect passwords
        #First try SQL code, then long random string,
        #then empty password, then exactly the length
        #limit for usernames and passwords
        response = self.client.post("/login", data=dict(username="admin", password="' OR 1=1--"), follow_redirects=True)
        assert "Welcome" not in response.data
       
        response = self.client.post("/login", data=dict(username="admin", password=urandom(1204)), follow_redirects=True)
        assert "Welcome" not in response.data
        
        response = self.client.post("/login", data=dict(username="admin", password=""), follow_redirects=True)
        assert "Welcome" not in response.data
        
        response = self.client.post("/login", data=dict(username="1", password=urandom(129)), follow_redirects=True)
        assert "Welcome" not in response.data
     
        #This case causes some type of error, can't figure out why 
        response = self.client.post("/login", data=dict(username=urandom(45), password=urandom(129)), follow_redirects=True)
        assert "Welcome" not in response.data

        #Log in as sales account
        response = self.client.post("/login", data=dict(username="Sales1", password="Test1"), follow_redirects=True)
        assert "Welcome" in response.data        
        
        #Log out of sales account
        response = self.client.get("/logout")
        assert "Welcome" not in response.data

        #Test with username and no password sent in post request
        response = self.client.post("/login", data=dict(username="Sales1"), follow_redirects=True)
        assert "Welcome" not in response.data

        #Barrage login functionality with completely
        #random input of random length over and over
        #"Fuzzing"
        for x in range(1001):
            response = self.client.post("/login", data=dict(username=urandom(randint(0, 300)),
                                                            password=urandom(randint(0,300))),
                                                            follow_redirects=True)
            assert "Welcome" not in response.data

    def test_register(self):
        """Unit test for register functionality
        """
        pass 
        

    def test_logout(self):
        """Unit test for logout functionality
        """
        pass

    def test_roles(self):
        """Unit test for role management functionality
        """
        pass

    #Tests that an anonymous user can not access certain pages
    def test_guest_access(self):

        #Test that guests can access home page
        response = self.client.get("/")
        assert response.status == "200 OK"

        #Test that guests can access login page
        response = self.client.get("/login")
        assert response.status == "200 OK"

        #Test that guests can access registration page
        response = self.client.get("/register")
        assert response.status == "200 OK"

        #Test that guests can not access logout page
        response = self.client.get("/logout")
        assert response.status != "200 OK"

        #Test that guests can not access roles page
        response = self.client.get("/roles")
        assert response.status != "200 OK"

        #Test that guests can not access addfeatures
        response = self.client.get("/addfeatures")
        assert response.status != "200 OK"  

        #Test that guests can not access carmanage page
        response = self.client.get("/carmanage")
        assert response.status != "200 OK" 
    
        #Test that guests can not access upload page
        response = self.client.get("/upload")
        assert response.status != "200 OK"

'''
    def tests_sales_access(self):
        
        #Create sales user by posting to registration page
        response = self.client.post("/register", data=dict(username="Salesman1", password="Test1", check="Test1"))
        assert "Registration Successful" in response.data 
        print response.data

        #Login as sales user
        response = self.client.post("/login", data=dict(username="Salesman1", password="Test1"), follow_redirects=True)
        assert "Welcome" in response.data 
'''

if __name__ == "__main__":
    unittest.main()
