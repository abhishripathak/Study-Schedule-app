# Use official Python image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (for PostgreSQL support)
RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && pip install --upgrade pip

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files into the container
COPY . .

# Expose Django's default port
EXPOSE 8000

# Command to run Django development server
CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8000"]
