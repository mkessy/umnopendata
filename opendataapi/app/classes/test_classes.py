from flask import Flask
from config import SQLALCHEMY_TEST_DATABASE_URI as testdb

import unittest
from pprint import pprint

from app import app, db
from app.classes.models import Uclass, Lecture

class ClassesTest(unittest.TestCase):

    def setUp(self):

        print 'creating app'
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = testdb
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):

        print 'tearing down db'
        db.session.remove()
        db.drop_all()

    def test_working(self):

        print 'YAY, a relatively simple'


if __name__ == '__main__':
    unittest.main()


