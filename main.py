import os
import logging
from flask import Flask, render_template_string, request, redirect, url_for, flash

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

# HTML Templates
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Career Portal</title>
    <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.css" rel="stylesheet">
    <style>
        .hero-section {
            position: relative;
            overflow: hidden;
        }
        .hero-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
        }
        .feather-sm {
            width: 16px;
            height: 16px;
            vertical-align: text-bottom;
        }
        .feather-lg {
            width: 32px;
            height: 32px;
            margin-bottom: 1rem;
        }
        .card {
            transition: transform 0.2s;
        }
        .card:hover {
            transform: translateY(-5px);
        }
        .footer {
            margin-top: auto;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index') }}">Career Portal</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('index') }}">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('job_listings') }}">Jobs</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('about') }}">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('contact') }}">Contact</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    {% block content %}{% endblock %}

    <footer class="footer mt-5 py-3 bg-dark">
        <div class="container text-center">
            <span class="text-muted">© 2024 Career Portal. All rights reserved.</span>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            feather.replace();
        });
    </script>
</body>
</html>
'''

INDEX_TEMPLATE = '''
{% extends "base.html" %}

{% block content %}
<div class="hero-section">
    <img src="https://images.unsplash.com/photo-1507679799987-c73779587ccf" class="w-100" style="height: 400px; object-fit: cover;" alt="Professional workplace">
    <div class="position-absolute top-50 start-50 translate-middle text-center">
        <h1 class="display-4 text-white">Find Your Dream Job</h1>
        <p class="lead text-white">Discover opportunities that match your skills and aspirations</p>
        <a href="{{ url_for('job_listings') }}" class="btn btn-primary btn-lg">Browse Jobs</a>
    </div>
</div>

<div class="container mt-5">
    <h2 class="text-center mb-4">Featured Jobs</h2>
    <div class="row">
        {% for job in featured_jobs %}
        <div class="col-md-4 mb-4">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">{{ job.title }}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">{{ job.company }}</h6>
                    <p class="card-text">{{ job.location }}</p>
                    <p class="card-text">{{ job.type }}</p>
                    <a href="{{ url_for('job_detail', job_id=job.id) }}" class="btn btn-outline-primary">Learn More</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>

    <div class="row mt-5">
        <div class="col-md-4 text-center">
            <img src="https://images.unsplash.com/photo-1543269664-56d93c1b41a6" class="rounded-circle mb-3" style="width: 150px; height: 150px; object-fit: cover;" alt="Career icon">
            <h3>Find Opportunities</h3>
            <p>Browse through hundreds of job listings</p>
        </div>
        <div class="col-md-4 text-center">
            <img src="https://images.unsplash.com/photo-1557804506-669a67965ba0" class="rounded-circle mb-3" style="width: 150px; height: 150px; object-fit: cover;" alt="Career icon">
            <h3>Apply Easily</h3>
            <p>Simple application process</p>
        </div>
        <div class="col-md-4 text-center">
            <img src="https://images.unsplash.com/photo-1455849318743-b2233052fcff" class="rounded-circle mb-3" style="width: 150px; height: 150px; object-fit: cover;" alt="Career icon">
            <h3>Grow Your Career</h3>
            <p>Take the next step in your professional journey</p>
        </div>
    </div>
</div>
{% endblock %}
'''

JOBS_TEMPLATE = '''
{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <h2 class="mb-4">Job Listings</h2>

    <form class="mb-4" method="GET" action="{{ url_for('job_listings') }}">
        <div class="input-group">
            <input type="text" class="form-control" name="search" placeholder="Search jobs..." value="{{ request.args.get('search', '') }}">
            <button class="btn btn-primary" type="submit">Search</button>
        </div>
    </form>

    <div class="row">
        {% for job in jobs %}
        <div class="col-md-6 mb-4">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">{{ job.title }}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">{{ job.company }}</h6>
                    <p class="card-text">
                        <i data-feather="map-pin" class="feather-sm me-1"></i> {{ job.location }}<br>
                        <i data-feather="clock" class="feather-sm me-1"></i> {{ job.type }}<br>
                        <i data-feather="dollar-sign" class="feather-sm me-1"></i> {{ job.salary_range }}
                    </p>
                    <div class="d-flex justify-content-between align-items-center">
                        <a href="{{ url_for('job_detail', job_id=job.id) }}" class="btn btn-outline-primary">View Details</a>
                        <a href="{{ url_for('apply', job_id=job.id) }}" class="btn btn-primary">Apply Now</a>
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
'''

JOB_DETAIL_TEMPLATE = '''
{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-8">
            <div class="card">
                <div class="card-body">
                    <h2 class="card-title">{{ job.title }}</h2>
                    <h5 class="card-subtitle mb-3 text-muted">{{ job.company }}</h5>

                    <div class="mb-4">
                        <p><i data-feather="map-pin" class="feather-sm me-1"></i> {{ job.location }}</p>
                        <p><i data-feather="clock" class="feather-sm me-1"></i> {{ job.type }}</p>
                        <p><i data-feather="dollar-sign" class="feather-sm me-1"></i> {{ job.salary_range }}</p>
                    </div>

                    <h5>Job Description</h5>
                    <p>{{ job.description }}</p>

                    <h5>Requirements</h5>
                    <ul>
                        {% for requirement in job.requirements %}
                        <li>{{ requirement }}</li>
                        {% endfor %}
                    </ul>

                    <a href="{{ url_for('apply', job_id=job.id) }}" class="btn btn-primary btn-lg">Apply Now</a>
                </div>
            </div>
        </div>

        <div class="col-md-4">
            <div class="card">
                <div class="card-body">
                    <h4 class="card-title">Company Information</h4>
                    <h6 class="card-subtitle mb-2">{{ company.name }}</h6>
                    <p class="card-text">{{ company.description }}</p>
                    <p class="card-text"><i data-feather="map-pin" class="feather-sm me-1"></i> {{ company.location }}</p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

APPLY_TEMPLATE = '''
{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-body">
                    <h2 class="card-title">Apply for {{ job.title }}</h2>
                    <h5 class="card-subtitle mb-4 text-muted">{{ job.company }}</h5>

                    <form method="POST" class="needs-validation" novalidate>
                        <div class="mb-3">
                            <label for="name" class="form-label">Full Name *</label>
                            <input type="text" class="form-control" id="name" name="name" required>
                        </div>

                        <div class="mb-3">
                            <label for="email" class="form-label">Email Address *</label>
                            <input type="email" class="form-control" id="email" name="email" required>
                        </div>

                        <div class="mb-3">
                            <label for="resume" class="form-label">Resume/CV Link *</label>
                            <input type="url" class="form-control" id="resume" name="resume" 
                                   placeholder="Link to your resume (Google Drive, Dropbox, etc.)" required>
                        </div>

                        <div class="mb-3">
                            <label for="cover_letter" class="form-label">Cover Letter</label>
                            <textarea class="form-control" id="cover_letter" name="cover_letter" rows="5"></textarea>
                        </div>

                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary">Submit Application</button>
                            <a href="{{ url_for('job_detail', job_id=job.id) }}" class="btn btn-outline-secondary">Back to Job Details</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

ABOUT_TEMPLATE = '''
{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-6">
            <h2>About Us</h2>
            <p class="lead">Connecting talented professionals with outstanding opportunities</p>
            <p>Career Portal is dedicated to helping job seekers find their dream careers and enabling companies to discover exceptional talent. Our platform provides a seamless connection between employers and candidates.</p>

            <h4 class="mt-4">Our Mission</h4>
            <p>To create meaningful connections in the professional world and facilitate career growth for individuals while helping organizations build strong teams.</p>
        </div>
        <div class="col-md-6">
            <img src="https://images.unsplash.com/photo-1496180470114-6ef490f3ff22" class="img-fluid rounded" alt="Team at work">
        </div>
    </div>

    <div class="row mt-5">
        <div class="col-md-4">
            <div class="card h-100">
                <div class="card-body text-center">
                    <i data-feather="users" class="feather-lg"></i>
                    <h4>For Job Seekers</h4>
                    <p>Access thousands of job opportunities from top companies across various industries.</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card h-100">
                <div class="card-body text-center">
                    <i data-feather="briefcase" class="feather-lg"></i>
                    <h4>For Employers</h4>
                    <p>Find the perfect candidates to join your team and grow your business.</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card h-100">
                <div class="card-body text-center">
                    <i data-feather="trending-up" class="feather-lg"></i>
                    <h4>Career Growth</h4>
                    <p>Resources and opportunities for professional development and advancement.</p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

CONTACT_TEMPLATE = '''
{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <h2 class="text-center mb-4">Contact Us</h2>

            <div class="card">
                <div class="card-body">
                    <div class="row mb-4">
                        <div class="col-md-4 text-center">
                            <i data-feather="mail" class="feather-lg"></i>
                            <h5>Email</h5>
                            <p>contact@careerportal.com</p>
                        </div>
                        <div class="col-md-4 text-center">
                            <i data-feather="phone" class="feather-lg"></i>
                            <h5>Phone</h5>
                            <p>+1 (555) 123-4567</p>
                        </div>
                        <div class="col-md-4 text-center">
                            <i data-feather="map-pin" class="feather-lg"></i>
                            <h5>Location</h5>
                            <p>San Francisco, CA</p>
                        </div>
                    </div>

                    <form method="POST">
                        <div class="mb-3">
                            <label for="name" class="form-label">Name</label>
                            <input type="text" class="form-control" id="name" required>
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" required>
                        </div>
                        <div class="mb-3">
                            <label for="subject" class="form-label">Subject</label>
                            <input type="text" class="form-control" id="subject" required>
                        </div>
                        <div class="mb-3">
                            <label for="message" class="form-label">Message</label>
                            <textarea class="form-control" id="message" rows="5" required></textarea>
                        </div>
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary">Send Message</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

# Flask routes
@app.route('/')
def index():
    featured_jobs = jobs[:3]  # Get first 3 jobs as featured
    return render_template_string(INDEX_TEMPLATE, featured_jobs=featured_jobs)

@app.route('/jobs')
def job_listings():
    search = request.args.get('search', '').lower()
    if search:
        filtered_jobs = [job for job in jobs if search in job['title'].lower() or search in job['company'].lower()]
    else:
        filtered_jobs = jobs
    return render_template_string(JOBS_TEMPLATE, jobs=filtered_jobs)

@app.route('/jobs/<int:job_id>')
def job_detail(job_id):
    job = next((job for job in jobs if job['id'] == job_id), None)
    if job:
        company = next((company for company in companies if company['name'] == job['company']), None)
        return render_template_string(JOB_DETAIL_TEMPLATE, job=job, company=company)
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
            applications.append(application)
            flash('Application submitted successfully!', 'success')
            return redirect(url_for('job_listings'))

    return render_template_string(APPLY_TEMPLATE, job=job)

@app.route('/about')
def about():
    return render_template_string(ABOUT_TEMPLATE)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template_string(CONTACT_TEMPLATE)

app.jinja_env.globals['base'] = BASE_TEMPLATE

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)