from flask import Blueprint

blue_print = Blueprint('main', __name__)

# Import các blueprint con cho API và Web
from .api import api_bp
from .web import web_bp

# Đăng ký blueprint con

# Application Interface
blue_print.register_blueprint(api_bp, url_prefix='/api')

# Web Interface
blue_print.register_blueprint(web_bp)
