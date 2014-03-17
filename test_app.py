#!/usr/bin/env python

#Unit test file for the Car Inventory Management System Application
import unittest
from flask.ext.testing import TestCase
 
from app import app, db


class MyTest(TestCase):
    
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class SomeTest(MyTest):
    
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

        ##
        #Still need to ask group about guest accessing carview
        ## 

        

        


        

if __name__ == "__main__":
    unittest.main()
