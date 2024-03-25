from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Job, UserJob, JobApplication
from flask_login import login_required, current_user
import time

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

@main.route('/jobs/applied', methods=['GET', 'POST'])
def jobs_applied():
    if request.method == 'POST':
        pass
    else:
        applied_jobs = UserJob.query.filter_by(user_id=current_user.id).all()  # Retrieve all UserJob objects for the current user
        applied_jobs_applied = [job for job in applied_jobs if job.status == 'Accepted'] # Filter applied jobs
        applied_jobs_declined = [job for job in applied_jobs if job.status == 'Declined'] # Filter declined jobs
        return render_template('jobs_applied.html', applied_jobs_applied=applied_jobs_applied, applied_jobs_declined=applied_jobs_declined)

@main.route('/decline_job/<int:job_id>', methods=['POST'])
def decline_job(job_id):
    from .models import UserJob, Job 
    job = Job.query.get_or_404(job_id)
    # Remove the UserJob entry to disassociate the user from the job
    user_job = UserJob.query.filter_by(user_id=current_user.id, job_id=job_id).first()
    UserJob.status = 'Declined'
    db.session.commit()
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

@main.route('/apply_job', methods=['POST'])
def apply_job():
    return render_template('job_application.html')

@main.route('/submit_application', methods=['POST'])
@login_required
def submit_application():
    expected_payment = request.form['expected_payment']
    cover_letter = request.form['cover_letter']
    other_details = request.form['other_details']
    if not expected_payment or not cover_letter:
        flash('Expected payment and cover letter cannot be empty', 'error')
        return render_template('job_application.html')
    
    new_application = JobApplication(expected_payment=expected_payment, cover_letter=cover_letter, other_details=other_details)
    db.session.add(new_application)
    user_job = UserJob.query.filter_by(user_id=current_user.id).first()
    if user_job:
        user_job.status = 'Accepted'
    db.session.commit()
    
    flash('Application successful!', 'success')
    
    return render_template('profile.html', name=current_user.name)
