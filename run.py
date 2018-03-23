import os

from app import create_app

# config_name = os.environ.get('FLASK_CONFIG')
# app = create_app(os.environ.get('FLASK_CONFIG'))
app = create_app()


# @app.route('/')
# def index():
#     return "<h1>Hello, world</>"


if __name__ == '__main__':
    app.run()
