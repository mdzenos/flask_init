from flask import Blueprint

api_bp = Blueprint('api', __name__)

# Import các phiên bản API
from .v1 import bp_v1
from .v2 import bp_v2

# Đăng ký các phiên bản API vào blueprint chính
api_bp.register_blueprint(bp_v1, url_prefix='/v1')
api_bp.register_blueprint(bp_v2, url_prefix='/v2')
