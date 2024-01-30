from config.database import Config

from flask import Flask
from flask_migrate import Migrate

from app.urls import api_bp, web_bp
from app.models import db
from app.models.users import Users
from common.exceptions import handle_exception

def create_app():
    app = Flask(__name__)

    # Load file config
    app.config.from_object(Config)

    # Register routes
    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)
    
    # Init database
    db.init_app(app)
    Migrate(app, db)
    
    # # Create database tables
    with app.app_context():
        db.create_all()

    @app.errorhandler(Exception)
    def handle_all_exceptions(error):
        return handle_exception(error)

    return app
