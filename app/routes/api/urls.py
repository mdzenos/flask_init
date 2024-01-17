from flask import Blueprint
from app.Authen.views import Authentication

api_bp = Blueprint('api', __name__)

api_bp.add_url_rule('/register', None, Authentication.register, methods=['POST'])
api_bp.add_url_rule('/login', None, Authentication.login, methods=['POST'])
api_bp.add_url_rule('/get_profile', None, Authentication.get_profile, methods=['GET'])
api_bp.add_url_rule('/get_all_user', None, Authentication.get_all_user, methods=['GET'])
api_bp.add_url_rule('/change_password', None, Authentication.change_password, methods=['POST'])
api_bp.add_url_rule('/delete_user', None, Authentication.delete_user, methods=['DELETE'])
api_bp.add_url_rule('/forget_password', None, Authentication.forget_password, methods=['POST'])
api_bp.add_url_rule('/set_password', None, Authentication.set_password, methods=['POST'])
