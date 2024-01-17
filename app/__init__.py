from config import Config

from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from app.models import db
from app.models.users import Users
from common.exceptions import handle_exception

def create_app():
    app = Flask(__name__)

    # Load file config
    app.config.from_object(Config)

    # Register routes
    from app.routes import blue_print
    app.register_blueprint(blue_print)

    # Init database
    db.init_app(app)
    migrate = Migrate(app, db)

    # # Create database tables
    with app.app_context():
        db.create_all()


    # @app.errorhandler(Exception)
    # def handle_all_exceptions(error):
    #     return handle_exception(error)
    # CORS(app)

    return app

