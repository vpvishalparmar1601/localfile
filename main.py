from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Flask app is running!'

if __name__ == '__main__':
    # Ensure Flask binds to all network interfaces inside the container (0.0.0.0)
    app.run(host='0.0.0.0', port=5000)
