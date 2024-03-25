from flask_login import UserMixin
from . import db
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=True)
    contact = Column(String(128), nullable=True)
    location = Column(String(128), nullable=True)
    # places = db.relationship('Place', backref='user', cascade='all, delete, delete-orphan')
    # reviews = db.relationship('Review', backref='user', cascade='all, delete, delete-orphan')
    # applied_jobs = db.relationship('Job', secondary='user_job')

class UserJob(db.Model):
    __tablename__ = "user_job"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status = db.Column(db.String(20)) # Accepted or Declined

    # Define a backref from Job to access users
    user = relationship('User', backref='user_jobs')
    job = relationship('Job', backref='user_jobs')

    # Define a relationship with Job explicitly
    job = relationship('Job', backref='applied_users')

class Job(db.Model):
    __tablename__ = "job"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(255), nullable=False)

    # Define a relationship with UserJob
    # user_jobs = relationship('UserJob', backref='job', cascade='all, delete-orphan')

    def __repr__(self):
        return f"Job(title={self.title}, description={self.description}, price={self.price}, category={self.category})"

class AppliedJob(db.Model):
    __tablename__ = "applied_job"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expected_payment = db.Column(db.String(100), nullable=False)
    cover_letter = db.Column(db.Text, nullable=False)
    other_details = db.Column(db.Text)
