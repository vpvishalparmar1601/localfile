# Base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY . .

# Expose port 5000
EXPOSE 5000

# Command to start Flask application
CMD ["python", "main.py"]
