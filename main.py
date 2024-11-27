from flask import Flask

# Create a Flask app instance
app = Flask(__name__)

# Define the home route
@app.route('/')
def home():
    return "Hello, Docker! Hello, world! This is Vishal Parmar's first file on a local server."

# Ensure the app runs when the script is executed directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Make the app accessible on all interfaces
