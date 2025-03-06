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
