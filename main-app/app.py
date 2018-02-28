from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1>Hello, world</>"

if __name__ == '__main__':
    app.run()