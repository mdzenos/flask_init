from flask import Blueprint
from app.authentication.views import Authentication as AuthView

bp = Blueprint('authentication', __name__)

bp.add_url_rule('/get_profile', None, AuthView.get_profile, methods=['GET'])
bp.add_url_rule('/get_all_user', None, AuthView.get_all_user, methods=['GET'])
bp.add_url_rule('/register', None, AuthView.register, methods=['POST'])
bp.add_url_rule('/login', None, AuthView.login, methods=['POST'])
bp.add_url_rule('/change_password', None, AuthView.change_password, methods=['POST'])
bp.add_url_rule('/forget_password', None, AuthView.forget_password, methods=['POST'])
bp.add_url_rule('/set_password', None, AuthView.set_password, methods=['POST'])
bp.add_url_rule('/delete_user', None, AuthView.delete_user, methods=['DELETE'])
