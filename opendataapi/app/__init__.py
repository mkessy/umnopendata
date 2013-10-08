from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# create Flask instances, link db to app
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


