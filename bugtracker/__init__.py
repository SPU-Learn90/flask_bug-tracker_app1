from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .main.routes import main
from .extensions import db


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    migrate = Migrate(app, db)

    db.init_app(app)
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
