from flask_login import UserMixin
from . import db
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric
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

    job_applications = db.relationship('JobApplication', backref='applicant', lazy='dynamic')

class UserJob(db.Model):
    __tablename__ = "user_job"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status = db.Column(db.String(20)) # Accepted or Declined
    title = db.Column(db.String(20))

    # Define a backref from Job to access users
    user = relationship('User', backref='user_jobs')
    job = relationship('Job', backref='user_jobs')

    # Define a relationship with Job explicitly
    job = relationship('Job', backref='applied_users')
    @property
    def job_title(self):
        return self.job.title

class Job(db.Model):
    __tablename__ = "job"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Define a relationship with UserJob
    user_jobs = relationship('UserJob', back_populates='job', cascade='all, delete-orphan')
    # Define a relationship with User
    user = relationship('User', backref='jobs')

    def __repr__(self):
        return f"Job(title={self.title}, description={self.description}, price={self.price}, category={self.category})"

class AppliedJob(db.Model):
    __tablename__ = "applied_job"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    expected_payment = db.Column(Numeric(10, 2), nullable=False)
    cover_letter = db.Column(db.Text, nullable=False)
    other_details = db.Column(db.Text)

    user = relationship('User', backref='job_applicants')
    job = db.relationship('Job', backref='job_applications')
