from app import create_app

app = create_app('config.DevelopmentConfig')


@app.route('/')
def index():
    return "<h1>Hello, world</>"


if __name__ == '__main__':
    app.run()
