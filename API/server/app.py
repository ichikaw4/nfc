from flask import Flask
from server.database import init_db
from .seeder import register_command
from .api import api


def create_app():
    app = Flask(__name__)
    app.config.from_object('server.config.Config')
    app.config['JSON_AS_ASCII'] = False
    init_db(app)
    register_command(app)
    app.register_blueprint(api)
    return app


app = create_app()


@app.route('/')
def hello_world():
    return 'Hello, World!'
