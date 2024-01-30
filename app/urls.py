from flask import Blueprint, render_template

from app.authentication.urls import bp as auth_bp
from common.constant import API_V1_PREFIX, API_V2_PREFIX

web_bp = Blueprint('web', __name__)
api_bp = Blueprint('api', __name__)

# Application Interface
api_bp.register_blueprint(auth_bp, url_prefix=f'{API_V1_PREFIX}/authentication')


# Web Interface
@web_bp.route('/')
def index():
    return render_template('views/index.html')
