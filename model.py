from flask_sqlalchemy import SQLAlchemy
# import sqlalchemy.engine
# from sqlalchemy import event
from flask import Flask
import os

## create table ##
# from model import db
# db.create_all()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

def create_app(app):
    db.init_app(app)
    db.app = app
    

# every time using sqlite, you must turn on foreign keys
# @event.listens_for(sqlalchemy.engine.Engine, 'connect')
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute('PRAGMA foreign_keys = ON')
#     cursor.close()

class User(db.Model):
    id = db.Column(db.String(30), primary_key=True)
    access_token = db.Column(db.String(60), nullable=False)
    access_token_secret = db.Column(db.String(60), nullable=False)
    tweet = db.relationship('Tweet', backref='user', lazy=True)

    def __init__(self, id, access_token, access_token_secret):
        self.id = id
        self.access_token = access_token
        self.access_token_secret = access_token_secret

class Tweet(db.Model):
    id = db.Column(db.String(30), primary_key=True)
    user_id = db.Column(db.String(30), db.ForeignKey('user.id'), nullable=False)
    delete_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, id, user_id, delete_time):
        self.id = id
        self.user_id = user_id
        self.delete_time = delete_time

