from flask import Blueprint
from app.controllers import example_controller

bp_v2 = Blueprint('v2', __name__)

# Định nghĩa các routes cho API phiên bản 2
@bp_v2.route('/endpoint')
def endpoint1():
    return example_controller.example_method()

