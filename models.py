from __boot__ import db
from sqlalchemy.dialects.postgresql import JSON
import datetime
from sqlalchemy.types import Integer, Boolean
from flask.ext.restless import APIManager


class Result(db.Model):
    __tablename__ = 'results'
    
    id = db.Column(db.Integer, primary_key=True)
    store = db.Column(db.String())
    product = db.Column(JSON)
    asin = db.Column(db.String())
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __init__(self, store, product, asin):
        self.store = store
        self.product = product
        self.asin = asin

    def __repr__(self):
        return '<id %r>' % self.id

class Uploads(db.Model):
    __tablename__ = 'uploads'

    email = db.Column(db.String())
    file = db.Column(JSON)
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, file, email):
        self.email = email
        self.file = file

    def __repr__(self):
        return '<id %r>' % self.id
