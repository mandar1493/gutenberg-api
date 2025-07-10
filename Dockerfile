FROM python:3.9-slim

# Set the working directory 
WORKDIR /code

# Copy the requirements
COPY ./requirements.txt /code/requirements.txt

# Install packages in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy application code
COPY ./app /code/app

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
