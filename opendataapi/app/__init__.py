from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import BASE_DIR

# create Flask instances, link DB to app
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)



