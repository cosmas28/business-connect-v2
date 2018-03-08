from flask import Flask


from src.resources.business import business_api
from src.resources.user import user_api

app = Flask(__name__)
app.register_blueprint(business_api, url_prefix='/api/v1')
app.register_blueprint(user_api, url_prefix='/api/v1')


@app.route('/')
def index():
    return "<h1>Hello, world</>"

if __name__ == '__main__':
    app.run(debug=True)