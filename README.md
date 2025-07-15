# Project Gutenberg Book API

A high-performance API for querying the Project Gutenberg e-book database, built with FastAPI and Docker.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/)
- [Python](https://www.python.org/downloads/) 3.9+

## Quickstart Guide

**1. Clone the repository:**
```bash
git clone [https://github.com/YOUR_USERNAME/gutenberg-api.git](https://github.com/YOUR_USERNAME/gutenberg-api.git)
cd gutenberg-api

2. Create Environment File:
Create a .env file in the project root with the following content:

DATABASE_URL="postgresql://gutenberg:password@localhost/gutenberg_dev"

3. Start the Database:
Launch the PostgreSQL database using Docker Compose.

docker-compose up -d

4. Load the Data:
Place your gutendex.dump file in the project root, then run these commands to load it into the database:

docker cp gutendex.dump gutenberg_db:/gutendex.dump
docker exec -it gutenberg_db psql -U gutenberg -d gutenberg_dev -f /gutendex.dump

5. Install Dependencies:
Set up a Python virtual environment and install the required packages.

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .\.venv\Scripts\activate

# Install packages
pip install -r requirements.txt

6. Run the API:
Start the local development server.

uvicorn app.main:app --reload

The API is now running at http://127.0.0.1:8000.

API Usage
Interactive Documentation
For a full list of endpoints and to test the API live, visit the interactive Swagger UI documentation at:
http://127.0.0.1:8000/docs

Example Request
Find books in English or French on the topic of "history" or "war":

curl -X GET "[http://127.0.0.1:8000/books?language=en,fr&topic=history,war](http://127.0.0.1:8000/books?language=en,fr&topic=history,war)"
