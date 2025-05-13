# Library Management System

This is a Flask-based Library Management System that allows you to manage books, members, and loans.

## Features

- Add, edit, delete, and view books
- Add, edit, delete, and view members
- Loan and return books
- Search books and members
- Responsive and modern UI using Tailwind CSS and Font Awesome
- REST API endpoints for searching books and members

## Requirements

- Python 3.7+
- Flask
- SQLAlchemy
- Werkzeug
- pandas (optional, used in some scripts)
- jupyter (optional, used in some scripts)

## Setup

1. Clone the repository.

2. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Initialize the database and add sample data:

```bash
python library_management/add_sample_data.py
```

## Running the Application

Run the Flask app on port 8000:

```bash
python library_management/app.py
```

The app will be accessible at `http://localhost:8000`.

## Environment Variables

- `SECRET_KEY`: (optional) Set a secret key for Flask session security. If not set, a random key will be generated on each run.

## Notes

- The app uses SQLite as the database (`library.db`).
- Debug mode is disabled for production readiness.
- Use the provided sample data script to populate the database with initial data.

## License

This project is licensed under the MIT License.
