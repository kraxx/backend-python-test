from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# configuration
DATABASE = '/tmp/alayatodo.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

import alayatodo.views