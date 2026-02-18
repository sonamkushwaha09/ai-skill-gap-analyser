# AI Resume Skill Gap Analyzer

A professional web application that analyzes resume skills against job descriptions using AI-powered matching.

## Features

- **User Authentication**: Secure login and signup system
- **PDF Resume Upload**: Extract text from PDF resumes
- **Skill Matching**: Compare resume skills with job requirements
- **Detailed Analysis**: View match percentage, matched skills, missing skills, and recommendations
- **Professional UI**: Modern, responsive design with Bootstrap

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. **Sign Up**: Create a new account
2. **Login**: Access your dashboard
3. **Upload Resume**: Upload your PDF resume
4. **Enter Job Description**: Paste the job description you want to analyze
5. **Get Results**: View your skill match analysis with recommendations

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Authentication**: Flask-Login
- **PDF Processing**: PyPDF2
- **UI Framework**: Bootstrap 5

## Features in Detail

### Skill Analysis
- Extracts skills from both resume and job description
- Calculates match percentage
- Identifies matched and missing skills
- Provides personalized recommendations for skill development

### Security
- Password hashing with Werkzeug
- Session-based authentication
- Secure file upload handling

### User Experience
- Drag-and-drop file upload
- Responsive design for all devices
- Intuitive navigation and clear results presentation