from flask import Blueprint
from app.controllers import example_controller

bp_v1 = Blueprint('v1', __name__)
# Định nghĩa các routes cho API phiên bản 1

@bp_v1.route('/endpoint', methods=['POST'])
def endpoint1():
    return example_controller.example_method()
