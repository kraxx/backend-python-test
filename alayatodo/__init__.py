from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv

# configuration
DATABASE = getenv('ALAYATODO_DATABASE', '/tmp/alayatodo.db')
SQLALCHEMY_DATABASE_URI = getenv('ALAYATODO_SQLALCHEMY_DATABASE_URI', 'sqlite:///' + DATABASE)
DEBUG = getenv('ALAYATODO_DEBUG', True)

PAGE_ITEM_LIMIT = getenv('ALAYATODO_PAGE_ITEM_LIMIT', 8)

SECRET_KEY = getenv('ALAYATODO_SECRET_KEY1', 'development key')
USERNAME = getenv('ALAYATODO_USERNAME', 'admin')
PASSWORD = getenv('ALAYATODO_PASSWORD', 'default')


app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

import alayatodo.views