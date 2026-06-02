# Job Track

A full-stack Job Application Tracking System built with Flask that helps job seekers organize applications, track interview progress, manage resumes, and schedule reminders from a single dashboard.

## Features

### Authentication

* User Registration
* Secure Login & Logout
* Forgot Password Support
* Password Reset Functionality

### Job Application Management

* Add New Applications
* Edit Application Details
* Delete Applications
* Track Application Status
* Store Company Information

### Interview Pipeline

* Visual Pipeline Tracking
* Application Status Monitoring
* Progress Management

### Resume Management

* Upload Resumes
* Manage Multiple Resumes
* Resume Organization

### Reminders & Calendar

* Schedule Follow-ups
* Interview Reminders
* Calendar Integration

### Analytics Dashboard

* Application Statistics
* Status-wise Distribution
* Activity Tracking
* Performance Insights

### User Profile & Settings

* Profile Management
* Theme Settings
* Account Preferences

## Tech Stack

### Backend

* Python
* Flask
* SQLAlchemy
* Flask-Migrate

### Database

* MySQL

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap

## Project Structure

```text
job-tracker/
│
├── app/
│   ├── models/
│   ├── routes/
│   ├── static/
│   └── templates/
│
├── migrations/
├── requirements.txt
├── config.py
├── run.py
└── setup_db.py
```

## Installation

### Clone Repository

```bash
git clone https://github.com/Karthik4765/Job-Track.git
cd Job-Track
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```

### Run Application

```bash
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

## Future Enhancements

* Email Notifications
* AI Resume Analysis
* Job Recommendation System
* Resume Scoring
* LinkedIn Integration
* Export Reports as PDF

## Author

Karthik Goud

GitHub: https://github.com/Karthik4765
