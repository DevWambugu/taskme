from flask import Blueprint
from . import db
from flask import render_template
from flask_login import login_required, current_user
from sqlalchemy import create_engine, Column, Integer, String
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import UserMixin
from . import db
from sqlalchemy import create_engine, Column, Integer, String

main = Blueprint('main', __name__)

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    contact = Column(String(128), nullable=False)
    location = Column(String(128), nullable=False)

main = Blueprint('main', __name__)
#Define Models

class Employer(db.Model):
    """Employer definitions"""
    __tablename__ = "employers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    contact = Column(String(128), nullable=False)

class Place(db.Model):
    """Maybe change to service ama?"""

    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.relationship('Review', backref='place', cascade='all, delete, delete-orphan')


class Service(db.Model):
    """Service class to store service information"""

    ___tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#    comments = db.relationship('Review', backref='service', cascade='all, delete, delete-orphan', foreign_keys='Review.place_id')

    def __repr__(self):
        return f'<Service {self.name}>'
    

class Review(db.Model):
    """ Review class to store review information """

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(String(1024), nullable=False)


    #Create A String
    def __repr__(self):
        return '<Name %r>' % self.name
    
# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")   


@main.route('/', strict_slashes=False)
def index():
    return render_template('/index.html')

@main.route('/registration.html', strict_slashes=False)
def registration_page():
    return render_template('registration.html')

@main.route('/index.html', strict_slashes=False)
@login_required
def profile():
    return render_template('profile.html, name=current_user.name')

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # Create the database tables
        db.create_all(extend_existing=True)
    app.run(host='0.0.0.0', port=5000)
