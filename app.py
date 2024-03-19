from flask import Blueprint, render_template
from . import db
from flask_login import login_required, current_user


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/listing_page')
def listing_page():
    return render_template('listing_page.html')

@main.route('/register_board')
def register_board():
    return render_template('register_board.html')
