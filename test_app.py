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
    
    def test_something(self):

        response = self.client.get("/carview")
        
        print response

        assert response

if __name__ == "__main__":
    unittest.main()
