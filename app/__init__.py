import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import routes, models, utils

def create_database(hard=False):
    ''' Creates the database schema specified by the SQLAlchemy models '''
    if hard:
        drop_database()

    print('Creating database schema ... ')
    db.create_all()
    print('Done!')

def drop_database():
    ''' Drops the current database schema '''
    print('Dropping database schema ... ')
    db.drop_all()
    print('Done!')


# AUTO SETUP
def _bootstrap_app_if_neccessary():
    db_path = _get_db_path()
    directory_path = '/'.join(db_path.split('/')[:-1])
    _make_sure_directory_exists(directory_path)
    _make_sure_database_exists(db_path)

def _get_db_path():
    ''' Returns the absolute url of the database '''
    return str(db.engine.url.database)

def _make_sure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def _make_sure_database_exists(path):
    if not os.path.exists(path):
        create_database()

_bootstrap_app_if_neccessary()