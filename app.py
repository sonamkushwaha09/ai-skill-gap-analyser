from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import PyPDF2
import re
from collections import Counter
import json
import webbrowser
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simple in-memory user storage (replace with database in production)
users = {}

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return users[user_id]
    return None

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def extract_skills(text):
    """Extract skills from text using keyword matching"""
    # Common skills database (expand this)
    skills_db = [
        'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
        'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express',
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git',
        'machine learning', 'ai', 'data science', 'tensorflow', 'pytorch',
        'agile', 'scrum', 'kanban', 'leadership', 'communication'
    ]
    
    text_lower = text.lower()
    found_skills = []
    
    for skill in skills_db:
        if skill in text_lower:
            found_skills.append(skill.title())
    
    return list(set(found_skills))  # Remove duplicates

def calculate_match_percentage(resume_skills, job_skills):
    """Calculate match percentage"""
    if not job_skills:
        return 0
    
    matched = set(resume_skills) & set(job_skills)
    return round((len(matched) / len(job_skills)) * 100, 1)

def get_missing_skills(resume_skills, job_skills):
    """Get skills present in job but missing in resume"""
    return list(set(job_skills) - set(resume_skills))

def get_recommendations(missing_skills):
    """Generate recommendations based on missing skills"""
    recommendations = []
    
    skill_recommendations = {
        'Python': 'Take an online Python course on Coursera or Udemy',
        'Java': 'Complete Java programming certification on Oracle',
        'JavaScript': 'Learn modern JavaScript through freeCodeCamp',
        'React': 'Build projects with React on Codecademy',
        'SQL': 'Practice SQL queries on LeetCode or HackerRank',
        'AWS': 'Get AWS Certified Cloud Practitioner certification',
        'Machine Learning': 'Enroll in Andrew Ng\'s Machine Learning course',
        'Docker': 'Complete Docker for Beginners tutorial on YouTube'
    }
    
    for skill in missing_skills:
        if skill in skill_recommendations:
            recommendations.append(f"{skill}: {skill_recommendations[skill]}")
        else:
            recommendations.append(f"{skill}: Research and learn through online tutorials")
    
    return recommendations

def open_browser():
    webbrowser.open('http://127.0.0.1:5000/')

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = users.get(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users:
            flash('Username already exists')
        else:
            hashed_password = generate_password_hash(password)
            user = User(username, username, hashed_password)
            users[username] = user
            flash('Account created successfully! Please log in.')
            return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/analyze', methods=['GET', 'POST'])
@login_required
def analyze():
    if request.method == 'POST':
        # Handle resume upload
        if 'resume' not in request.files:
            flash('No resume file uploaded')
            return redirect(request.url)
        
        resume_file = request.files['resume']
        job_description = request.form.get('job_description')
        
        if resume_file.filename == '':
            flash('No resume file selected')
            return redirect(request.url)
        
        if resume_file and resume_file.filename.lower().endswith('.pdf'):
            filename = secure_filename(resume_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume_file.save(file_path)
            
            # Extract text and skills from resume
            resume_text = extract_text_from_pdf(file_path)
            resume_skills = extract_skills(resume_text)
            
            # Extract skills from job description
            job_skills = extract_skills(job_description)
            
            # Calculate match
            match_percentage = calculate_match_percentage(resume_skills, job_skills)
            matched_skills = list(set(resume_skills) & set(job_skills))
            missing_skills = get_missing_skills(resume_skills, job_skills)
            recommendations = get_recommendations(missing_skills)
            
            # Clean up uploaded file
            os.remove(file_path)
            
            return render_template('results.html', 
                                 match_percentage=match_percentage,
                                 matched_skills=matched_skills,
                                 missing_skills=missing_skills,
                                 recommendations=recommendations)
        else:
            flash('Please upload a PDF file')
    
    return render_template('analyze.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
