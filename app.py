from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Job, UserJob, JobApplication, User
from flask_login import login_required, current_user
import time

main = Blueprint('main', __name__)

@main.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/about_us')
def about_us():
    return render_template('about.html')

@main.route('/jobs/posted')
@login_required
def jobs_posted():
    # Retrieve all posted jobs from the database
#    jobs = Job.query.all()
    selected_category = request.args.get('category')
    if selected_category and selected_category != 'All Categories':
        jobs = Job.query.filter_by(category=selected_category).all()
    else:
        jobs = Job.query.all()
    categories = {job.category for job in Job.query.all()}
    return render_template('jobs_posted.html', jobs=jobs, categories=categories, selected_category=selected_category)

@main.route('/jobs/applied', methods=['GET', 'POST'])
def jobs_applied():
    if request.method == 'POST':
        # future possibility
        # have a form for applying and declining
        pass
    else:
        applied_jobs = UserJob.query.filter_by(user_id=current_user.id).all()  # Retrieve all UserJob objects for the current user
        applied_jobs_applied = [user_job.job.title for user_job in applied_jobs if user_job.status == 'Accepted' or user_job.status == 'Applied'] # Filter applied jobs
        applied_jobs_declined = [user_job.job.title for user_job in applied_jobs if user_job.status == 'Declined'] # Filter declined jobs
        return render_template('jobs_applied.html', applied_jobs_applied=applied_jobs_applied, applied_jobs_declined=applied_jobs_declined)

@main.route('/decline_job/<int:job_id>', methods=['POST'])
def decline_job(job_id):
    from .models import UserJob, Job
    job = Job.query.get_or_404(job_id)
    # Fetch the UserJob entry to update the status
    user_job = UserJob.query.filter_by(user_id=current_user.id, job_id=job_id).first()
    if user_job:
        user_job.status = 'Declined'
        db.session.commit()
        flash('You have declined the job.')
    return redirect(url_for('main.jobs_applied'))

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

        # Ensure user is logged in before creating the job
        if current_user.is_authenticated:

            # Create the job with the user_id set to the current user's ID
            post_job = Job(title=title, description=description, price=price, category=category, user_id=current_user.id)
            db.session.add(post_job)
            db.session.commit()

            # FLash success message
            flash('Job Posted Successfully', 'success')

            # Redirect to jobs_posted.html
            return redirect(url_for('main.jobs_posted'))
        else:
            flash('Please log in to post a job', 'error')
            return redirect(url_for('main.jobs_posted'))
    else:
        # Render the form for GET requests
        return render_template('register_board.html')

@main.route('/job_details/<int:job_id>')
def job_details(job_id):
    # Retrieve the job details from the database
    job = Job.query.get_or_404(job_id)
    return render_template('job_details.html', job=job)

@main.route('/applicant_details/<int:job_application_id>')
def applicant_details(job_application_id):
    # Retrieve the job application details from the database
    job_application = JobApplication.query.get_or_404(job_application_id)
    
    # Get the user corresponding to this job application
    user = job_application.user
    
    if user is None:
        # Handle the case where user is not found
        flash('User not found for this job application.', 'error')
        return redirect(url_for('main.index'))
    
    # Get all user jobs for this user
    user_jobs = user.user_jobs if user.user_jobs else []
    
    # Find the user job corresponding to this job application
    for user_job in user_jobs:
        if user_job.status == 'Applied' or user_job.status == 'Accepted':
            job = user_job.job
            break
    else:
        # If no relevant user job found, handle the case here
        job = None
    
    return render_template('job_applicants.html', job=job, job_application=job_application)

@main.route('/jobs/<int:job_id>/applicants')
@login_required
def job_applicants(job_id):
    job = Job.query.get_or_404(job_id)
    if job.user_id != current_user.id:
        # Ensure that only the user who posted the job can view the applicants
        flash('Only the employer can view this.', 'error')
        #return redirect(url_for('main.jobs_posted'))

    applicants = UserJob.query.filter((UserJob.job_id == job_id) & ((UserJob.status == 'Applied') | (UserJob.status == 'Accepted'))).all()
    return render_template('job_applicants.html', job=job, applicants=applicants)

@main.route('/apply_job/<int:job_id>', methods=['POST'])
def apply_job(job_id):
    if not current_user.is_authenticated:
        flash('Please log in to apply for jobs.', 'error')
        return redirect(url_for('auth.login'))
    if current_user.is_authenticated:
        # Check if the user has already applied for this job
        job = Job.query.get_or_404(job_id)  # Fetch the job details
        existing_user_job = UserJob.query.filter_by(user_id=current_user.id, job_id=job_id).first()
        if existing_user_job:
            flash('You have already applied for this job.')
            jobs = Job.query.all()
            return render_template('listing_page.html', jobs=jobs)
        #else:
        #    return render_template('job_application.html')

        else:
            # Create a new UserJob instance
            new_user_job = UserJob(user_id=current_user.id, job_id=job_id, status='Applied')
            # Add it to the database session
            db.session.add(new_user_job)
            db.session.commit()
            flash('You have successfully applied for the job.')

            return render_template('job_application.html', job=job)

@main.route('/submit_application', methods=['POST'])
@login_required
def submit_application():
    # Retrieving form data
    expected_payment = request.form['expected_payment']
    cover_letter = request.form['cover_letter']
    other_details = request.form['other_details']
    job_title = request.form['job_title']
    job_id = request.form['job_id']

    # Validation
    if not expected_payment or not cover_letter:
        flash('Expected payment and cover letter cannot be empty', 'error')
        return render_template('job_application.html')
    
    # Creating a new JobApplication instance and assigning user_id
    new_application = JobApplication(
        job_id=job_id,
        title=job_title,
        expected_payment=expected_payment,
        cover_letter=cover_letter, 
        other_details=other_details,
        user_id=current_user.id
    )
    db.session.add(new_application)

    # Updating the status of the UserJob to 'Accepted'
    user_job = UserJob.query.filter_by(user_id=current_user.id).first()
    if user_job:
        user_job.status = 'Accepted'
        db.session.commit()

    flash('Application successful!', 'success')

    return render_template('profile.html', name=current_user.name)

@main.route('/job_applicants', methods=['GET'])
@login_required
def get_applications():
    job_applications = JobApplication.query.all()
    return render_template('job_applications.html', job_applications=job_applications)

@main.route('/user_details/<int:user_id>')
def user_details(user_id):
    # Retrieve the applicant details from the database
    user = User.query.get_or_404(user_id)
    job_id = request.args.get('job_id')

    if job_id:
        # Fetch the job details based on the provided job_id
        job = Job.query.get_or_404(job_id)

        # Fetch the query object associated with job_applications relationship for the current job
        job_applications_query = user.job_applications.filter_by(job_id=job_id).all()
    else:
        # If no job id provided, fetch all job applications for the user
        job = None
        job_applications_query = []

    return render_template('user_details.html', user=user, job_applications=job_applications_query, job=job)

