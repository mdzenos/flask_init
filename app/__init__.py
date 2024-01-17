from config.environment import Config

from flask import Flask
from flask_migrate import Migrate

from app.models import db
from app.models.users import Users
from common.exceptions import handle_exception

def create_app():
    app = Flask(__name__)

    # Load file config
    app.config.from_object(Config)

    # Register routes
    from app.routes.urls import main_bp
    app.register_blueprint(main_bp)
    
    # Init database
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # # Create database tables
    with app.app_context():
        db.create_all()

    @app.errorhandler(Exception)
    def handle_all_exceptions(error):
        return handle_exception(error)

    return app
