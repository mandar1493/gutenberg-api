# Project Gutenberg Book API

An FastAPI API Project For Gutenberg e-book database, built with Postgres and docker.

1. Install Dependencies:
Set up a Python virtual environment and install the required packages.

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate 

# Install packages
pip install -r requirements.txt


## Features
- Filter by title, language, author, etc.
- Pagination and popularity sorting
- Swagger docs at `/docs`