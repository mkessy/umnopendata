from flask.ext.testing import TestCase
import unittest
from flask import Flask
from config import SQLALCHEMY_TEST_DATABASE_URI as testdb

from pprint import pprint

from app import db
from app.classes.models import Uclass, Lecture

class ClassesTest(TestCase):

    def create_app(self):

        print 'creating app'

        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = testdb
        print app.config

        return app

    def setUp(self):

        print 'setting up db'

        db.create_all()

    def tearDown(self):

        print 'tearing down db'

        db.session.remove()
        db.drop_all()


    def test_working(self):

        pprint(db.__dict__)
        print 'YAY, a relatively simple'


if __name__ == '__main__':
    unittest.main()


