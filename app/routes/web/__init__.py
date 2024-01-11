from flask import Blueprint, render_template

web_bp = Blueprint('web', __name__)


# Định nghĩa các routes cho Web
@web_bp.route('/')
def home():
    return render_template('views/index.html')


@web_bp.route('/login')
def login():
    return 'Login Page'
