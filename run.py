from flasgger import Swagger

from app import create_app

app = create_app('config.DevelopmentConfig')
swagger = Swagger(app)

@app.route('/')
def index():
    return '<h1>Hello, world</>'


if __name__ == '__main__':
    app.run()
