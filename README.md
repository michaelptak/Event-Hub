# Event-Hub
Full-stack event discovery web application built with Django using Ticketmaster API

## Live Demo
**[View Live Site](https://event-hub-0yzz.onrender.com/)**
*Note: Free tier may take up to 30-60 seconds to wake up on first visit*

## Features
- Event search using Ticketmaster API
- User authentication (signup/login/logout)
- Favorites system with AJAX operations
- Dark mode toggle with localStorage persistence
- Responsive design with Bootstrap

## Tech Stack
- **Backend:** Django 4.2, Python
- **Database:** PostgreSQL (production database), using Django ORM for database operations
- **Frontend:** HTML/CSS, JavaScript (Vanilla + AJAX)
- **Styling:** Bootstrap 5

## Running Locally

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- PostgreSQL (optional, SQLite will be used by default for local development)

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd Event-Hub
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and configure the following variables:
- `DJANGO_SECRET_KEY`: Generate a new secret key for development
- `TICKETMASTER_API_KEY`: Get your API key from https://developer.ticketmaster.com/
- `DEBUG`: Set to `True` for local development
- `ALLOWED_HOSTS`: Keep as `localhost,127.0.0.1` for local development

5. Run database migrations
```bash
python manage.py migrate
```

6. Create a superuser (optional, for admin access)
```bash
python manage.py createsuperuser
```

7. Start the development server
```bash
python manage.py runserver
```

The application will be available at http://localhost:8000/

### Database Configuration

By default, the application uses SQLite for local development. If you want to use PostgreSQL locally, add the following to your `.env` file:
```
DATABASE_URL=postgres://username:password@localhost:5432/eventhub
```

## Project Context
Built as final project for CS416 Web Development course at Central Connecticut State University.
