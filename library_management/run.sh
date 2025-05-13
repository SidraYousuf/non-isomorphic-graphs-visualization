#!/bin/bash

# Run the Flask app on port 8000
export FLASK_APP=library_management/app.py
export FLASK_ENV=production
export SECRET_KEY="your-production-secret-key"

python3 library_management/app.py
