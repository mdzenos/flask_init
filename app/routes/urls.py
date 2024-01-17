from flask import Blueprint

from app.routes.api.urls import api_bp

main_bp = Blueprint('main', __name__)


# Application Interface
main_bp.register_blueprint(api_bp, url_prefix='/api')

