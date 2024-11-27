from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'hello my applicaton is deployed'

if __name__ == '__main__':
    # Change the host to 0.0.0.0 so it's accessible from outside the container
    app.run(host='0.0.0.0', port=5000)
