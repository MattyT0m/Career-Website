import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_key")

# In-memory data storage
companies = [
    {
        'name': 'Tech Corp',
        'description': 'Leading technology solutions provider',
        'location': 'San Francisco, CA'
    },
    {
        'name': 'Design Studio',
        'description': 'Creative design agency',
        'location': 'New York, NY'
    },
    {
        'name': 'Finance Pro',
        'description': 'Financial services company',
        'location': 'Chicago, IL'
    }
]

jobs = [
    {
        'id': 1,
        'title': 'Senior Software Engineer',
        'company': 'Tech Corp',
        'location': 'San Francisco, CA',
        'type': 'Full-time',
        'description': 'We are looking for an experienced software engineer to join our team.',
        'requirements': ['5+ years experience', 'Python', 'JavaScript', 'Cloud platforms'],
        'salary_range': '$120,000 - $180,000'
    },
    {
        'id': 2,
        'title': 'UI/UX Designer',
        'company': 'Design Studio',
        'location': 'New York, NY',
        'type': 'Full-time',
        'description': 'Join our creative team as a UI/UX designer.',
        'requirements': ['3+ years experience', 'Figma', 'User research', 'Prototyping'],
        'salary_range': '$90,000 - $130,000'
    },
    {
        'id': 3,
        'title': 'Financial Analyst',
        'company': 'Finance Pro',
        'location': 'Chicago, IL',
        'type': 'Full-time',
        'description': 'Seeking a financial analyst to join our growing team.',
        'requirements': ['2+ years experience', 'Excel', 'Financial modeling', 'MBA preferred'],
        'salary_range': '$70,000 - $100,000'
    },
    {
        'id': 4,
        'title': 'Product Manager',
        'company': 'Tech Corp',
        'location': 'San Francisco, CA',
        'type': 'Full-time',
        'description': 'Lead product development and strategy.',
        'requirements': ['4+ years experience', 'Technical background', 'Agile methodologies'],
        'salary_range': '$130,000 - $180,000'
    }
]

applications = []

def save_application(application):
    applications.append(application)

@app.route('/')
def index():
    featured_jobs = jobs[:3]  # Get first 3 jobs as featured
    return render_template('index.html', featured_jobs=featured_jobs)

@app.route('/jobs')
def job_listings():
    search = request.args.get('search', '').lower()
    if search:
        filtered_jobs = [job for job in jobs if search in job['title'].lower() or search in job['company'].lower()]
    else:
        filtered_jobs = jobs
    return render_template('jobs.html', jobs=filtered_jobs)

@app.route('/jobs/<int:job_id>')
def job_detail(job_id):
    job = next((job for job in jobs if job['id'] == job_id), None)
    if job:
        company = next((company for company in companies if company['name'] == job['company']), None)
        return render_template('job_detail.html', job=job, company=company)
    return redirect(url_for('job_listings'))

@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply(job_id):
    job = next((job for job in jobs if job['id'] == job_id), None)
    if not job:
        return redirect(url_for('job_listings'))

    if request.method == 'POST':
        if not all([request.form.get('name'), request.form.get('email'), request.form.get('resume')]):
            flash('Please fill in all required fields', 'error')
        else:
            application = {
                'job_id': job_id,
                'name': request.form['name'],
                'email': request.form['email'],
                'resume': request.form['resume'],
                'cover_letter': request.form.get('cover_letter', '')
            }
            save_application(application)
            flash('Application submitted successfully!', 'success')
            return redirect(url_for('job_listings'))

    return render_template('apply.html', job=job)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
