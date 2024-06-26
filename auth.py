from flask_login import login_user, login_required, logout_user
from flask import Blueprint, render_template, redirect, url_for, flash, request
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    '''code to validate and add user to database goes here'''
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    '''if this returns a user, then the email already exists in database'''
    user = User.query.filter_by(email=email).first()
    '''if a user is found, we want to redirect back to signup page so user can try again'''
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    '''create a new user with the form data. Hash the password so the plaintext version isn't saved.'''
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

    '''add the new user to the database'''
    db.session.add(new_user)
    db.session.commit()
    flash('Successfully Registered')
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        '''if the user doesn't exist or password is wrong, reload the page'''
        return redirect(url_for('auth.login')) 

    '''if the above check passes, then we know the user has the right credentials'''
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
