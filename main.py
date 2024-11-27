from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Flask app is running!'

if __name__ == '__main__':
    # Flask binds to all interfaces (0.0.0.0) for Docker compatibility
    app.run(host='0.0.0.0', port=5000)
