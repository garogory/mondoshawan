# models.py

from flask_login import UserMixin
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Float, Integer, Column
from . import db

#Base = declarative_base()

class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = Column(String(100), unique=True)
    password = Column(String(100))
    name = Column(String(1000))

class Entry(UserMixin, db.Model):
    id = Column(Integer, primary_key=True) # primary keys are required by SQLAlchemy
    address = Column(String(500), unique=True)
    latitude = Column(Float(), unique=True)
    longitude = Column(Float(), unique=True)
