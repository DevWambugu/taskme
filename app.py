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
    applied_jobs = current_user.applied_jobs
    return render_template('jobs_applied.html', applied_jobs=applied_jobs)

@main.route('/decline_job/<int:job_id>', methods=['POST'])
def decline_job(job_id):
    from .models import UserJob
    job = Job.query.get_or_404(job_id)
    # Remove the UserJob entry to disassociate the user from the job
    user_job = UserJob.query.filter_by(user_id=current_user.id, job_id=job_id).first()
    if user_job:
        db.session.delete(user_job)
        db.session.commit()
        flash('You have declined the job.')
    return redirect(url_for('main.index'))

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/listing_page')
def listing_page():
    # Retrieve all posted jobs from the database
    jobs = Job.query.all()
    return render_template('listing_page.html', jobs=jobs)

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

@main.route('/job_details/<int:job_id>')
def job_details(job_id):
    # Retrieve the job details from the database
    job = Job.query.get_or_404(job_id)
    return render_template('job_details.html', job=job)

@main.route('/apply_job/<int:job_id>', methods=['POST'])
def apply_job(job_id):
    flash('You have successfully applied for the job.')
    return redirect(url_for('main.index'))
