from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Job
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/jobs/posted')
@login_required
def jobs_posted():
    # Retrieve all posted jobs from the database
    jobs = Job.query.all()
    return render_template('jobs_posted.html', jobs=jobs) # Pass jobs data to the template

@main.route('/jobs/applied')
def jobs_applied():
    return render_template('jobs_applied.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/listing_page')
def listing_page():
    return render_template('listing_page.html')

@main.route('/register_board', methods=['GET', 'POST'])
def register_board():
    from .models import Job
    if request.method == 'POST':
        # Handle for submission
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        category = request.form.get('category')

        # Save form data to a database
        post_job = Job(title=title, description=description, price=price, category=category)
        db.session.add(post_job)
        db.session.commit()

        # FLash success message
        flash('Job Posted Successfully'), 200

        # Redirect to jobs_posted.html
        return redirect(url_for('main.jobs_posted'))
    else:
        # Render the form for GET requests
        return render_template('register_board.html')
