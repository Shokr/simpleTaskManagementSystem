import unittest

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config.config import Config

db = SQLAlchemy()


def run_tests():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # Register blueprints
    from api import api_bp
    app.register_blueprint(api_bp)
    migrate = Migrate(app, db)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
