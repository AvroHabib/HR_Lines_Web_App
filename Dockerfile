# Use the official Python image
FROM python:3.10-slim

# Install system dependencies for MySQL and pkg-config
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . /app/

# Expose port 8000 to access the Django app
EXPOSE 8000

# Run Django's built-in server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
