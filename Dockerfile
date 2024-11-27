FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the app files
COPY . .

# Expose port 5000 to the host
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "main.py"]
