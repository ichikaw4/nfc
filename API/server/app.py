from flask import Flask
from server.database import init_db
from .seeder import register_command


def create_app():
    app = Flask(__name__)
    app.config.from_object('server.config.Config')
    init_db(app)
    register_command(app)
    return app


app = create_app()


@app.route('/')
def hello_world():
    return 'Hello, World!'
