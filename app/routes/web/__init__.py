from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session
from app.models import Users
from cerberus import Validator
from common.encrypt import PassWordManager

web_bp = Blueprint('web', __name__)
regist_schema = {
    'username': {'type': 'string', 'minlength': 5, 'maxlength': 20, 'required': True},
    'email': {'type': 'string', 'regex': r'\S+@\S+\.\S+', 'required': True},
    'password': {'type': 'string', 'minlength': 6, 'required': True},
    'repassword': {'type': 'string', 'minlength': 6, 'required': True}
}
login_schema = {
    'username': {'type': 'string', 'minlength': 5, 'maxlength': 20, 'required': True},
    'password': {'type': 'string', 'minlength': 6, 'required': True},
}
regist_validator = Validator(regist_schema)
login_validator = Validator(login_schema)


# Định nghĩa các routes cho Web
@web_bp.route('/')
def index():
    return render_template('views/index.html')


@web_bp.route('/dashboard')
def dashboard():
    x = session.keys()
    print(x)
    return render_template('views/auth/dashboard.html', form_data=x)


@web_bp.route('/login', methods=['GET', 'POST'])
def login():
    form_data = {}
    if request.method == 'POST':
        # if request.headers['Content-Type'] == 'application/json':
        #     data = request.json
        #     username = data['username']
        #     password = data['password']
        # else:
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if request.method == 'POST':
            data = {'username': username, 'password': password}

            if login_validator.validate(data):
                user_info = Users.query.filter_by(username=username).first()
                if user_info is None:
                    flash('Username don\'t exists.', 'danger')
                    return redirect(url_for('main.web.login'))
                elif PassWordManager.check_password(password, user_info.password) == False:
                    flash('Password Invalid.', 'danger')
                    return redirect(url_for('main.web.login'))
                else:
                    Users.store(username=username, password=password)
                    flash('Login successfully!', 'success')
                    return redirect(url_for('main.web.dashboard'))
            else:
                form_data = data.copy()
                for field, errors in login_validator.errors.items():
                    for error in errors:
                        flash(f"Error in {field}: {error}", 'danger')


    return render_template('views/auth/login.html', form_data=form_data)


@web_bp.route('/register', methods=['GET', 'POST'])
def register():
    form_data = {}
    if request.method == 'POST':
        fullname = request.form.get('fullname', '')
        username = request.form.get('username', '')
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        repassword = request.form.get('repassword', '')
        data = {'username': username, 'email': email, 'password': password, 'repassword': repassword}

        if regist_validator.validate(data):
            if password != repassword:
                flash('Passwords do not match', 'danger')
                return redirect(url_for('main.web.register'))
            elif Users.query.filter_by(username=username).first():
                flash('Username already exists. Please choose another.', 'danger')
                return redirect(url_for('main.web.register'))
            elif Users.query.filter_by(email=email).first():
                flash('Email already exists. Please choose another.', 'danger')
                return redirect(url_for('main.web.register'))
            else:
                Users.create(fullname=fullname, username=username, email=email, password=password)
                flash('User registered successfully!', 'success')
                return redirect(url_for('main.web.login'))
        else:
            form_data = data.copy()
            form_data['fullname'] = fullname
            for field, errors in regist_validator.errors.items():
                for error in errors:
                    flash(f"Error in {field}: {error}", 'danger')

    return render_template('views/auth/register.html', form_data=form_data)


@web_bp.route('/forgot', methods=['GET', 'POST'])
def forgot():
    return render_template('views/auth/forgot.html')


@web_bp.route('/logout')
def logout():
    # logout_user()
    flash('Logout successful', 'success')
    return redirect(url_for('main.web.index'))
