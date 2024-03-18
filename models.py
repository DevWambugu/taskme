from flask_login import UserMixin
from . import db
from sqlalchemy import create_engine, Column, Integer, String

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=True)
    contact = Column(String(128), nullable=True)
    location = Column(String(128), nullable=True)
    #places = db.relationship('Place', backref='user', cascade='all, delete, delete-orphan')
    #reviews = db.relationship('Review', backref='user', cascade='all, delete, delete-orphan')
