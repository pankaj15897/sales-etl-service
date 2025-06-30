# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED True
ENV PORT 8080

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run tests during build
RUN python -m unittest test_etl.py

# Run the web service
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app