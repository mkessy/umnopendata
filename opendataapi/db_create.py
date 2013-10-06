#!/home/mepuka/.virtualenvs/opendataapi/bin/python
from config import SQLALCHEMY_DATABASE_URI
from app import db

# create the database
db.create_all()
