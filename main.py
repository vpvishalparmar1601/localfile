from flask import FlaskS

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Docker! Hello, world! This is a vishal parmar the first file in local server."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)