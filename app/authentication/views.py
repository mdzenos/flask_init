import smtplib
import logging

from flask import jsonify, request
from datetime import datetime
from cerberus import Validator
from email.mime.text import MIMEText

from app.models import Users
from config.database import Config
from config.logging import Log

from common.status_code import StatusCode
from common.constant import user_login_schema, user_registration_schema, user_password_schema, username_schema, \
    password_schema, LOG_TYPE

from common.encrypt import PassWordManager, JWTAppManager


class Authentication:
    @staticmethod
    def construct_response(message, result=None, status_code=StatusCode.HTTP_INTERNAL_SERVER_ERROR, header_token=None):
        response_data = {
            'response': {
                'message': message,
                'result': result
            }
        }
        headers = {
            'Content-Type': 'application/json',
        }
        if header_token is not None:
            headers['XSRF-Token'] = header_token
        response = jsonify(response_data)
        response.headers = headers
        response.status_code = status_code
        return response

    @staticmethod
    def register():
        data = request.json
        validate = Validator(user_registration_schema)
        if not validate.validate(data):
            return Authentication.construct_response('Validation Error', validate.errors, StatusCode.HTTP_BAD_REQUEST)

        fullname = data.get('fullname')
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        user = Users.create(fullname, username, password, email)
        new_user = Authentication.copy_dict(user.to_dict(), ["email", "fullname", "username"])
        create_token = Users.save_new_token(user.id)
        if create_token is not None:
            token = create_token.json
            new_user['access_token'] = token.get('access_token', None)
            return Authentication.construct_response('success', new_user, StatusCode.HTTP_OK)
        return Authentication.construct_response('error', "Have error in process create account",
                                                 StatusCode.HTTP_INTERNAL_SERVER_ERROR)

    @staticmethod
    def login():
        Log.write(__name__, LOG_TYPE.get("INFO", "info"), 'Start login', request)
        data = request.json
        validate = Validator(user_login_schema)
        if not validate.validate(data):
            return Authentication.construct_response('Validation Error', validate.errors, StatusCode.HTTP_BAD_REQUEST)

        username = data.get('username')
        password = data.get('password')

        user = Users.get_user(username=username)
        if user is None:
            return Authentication.construct_response('User not found', None, StatusCode.HTTP_NOT_FOUND)

        check_login = PassWordManager.check_password(password, user.password)
        if check_login is False:
            return Authentication.construct_response('Password invalid', None, StatusCode.HTTP_UNAUTHORIZED)

        user_info = Authentication.copy_dict(user.to_dict(), ["email", "fullname", "username"])
        create_token = Users.save_new_token(user.id)
        if create_token is not None:
            token = create_token.json
            user_info['access_token'] = token.get('access_token', None)
            return Authentication.construct_response('success', user_info, StatusCode.HTTP_OK)
        return Authentication.construct_response('error', "Have error in process create account",
                                                 StatusCode.HTTP_BAD_REQUEST)

    @staticmethod
    def change_password():
        data = request.json
        validate = Validator(user_password_schema)
        if not validate.validate(data):
            return Authentication.construct_response('Validation Error', validate.errors, StatusCode.HTTP_BAD_REQUEST)

        old_password = data.get('old_password')
        new_password = data.get('new_password')
        if old_password == new_password:
            return Authentication.construct_response('New password is same as old password', new_password)

        token = request.headers.get('XSRF-Token', None)
        if token is None:
            return Authentication.construct_response('Haven\'t access token', None, StatusCode.HTTP_UNAUTHORIZED)
        payload = JWTAppManager.decode_token(token)
        user_id = payload.get('uid')
        verify_token = Authentication.verify_token(token)
        if verify_token is None:
            return Authentication.construct_response('Token invalid or expired!!!', None, StatusCode.HTTP_FORBIDDEN)

        user_info = Users.get_user(id=user_id)
        check_password = PassWordManager.check_password(old_password, user_info.password)
        if check_password is False:
            return Authentication.construct_response("Old password is incorrect", None, StatusCode.HTTP_NOT_FOUND)
        Users.update(id=user_id, password=new_password)
        return Authentication.construct_response("Password changed", new_password, StatusCode.HTTP_OK, verify_token)

    @staticmethod
    def get_profile():
        token = request.headers.get('XSRF-Token', None)
        if token is None:
            return Authentication.construct_response('Haven\'t access token', None, StatusCode.HTTP_UNAUTHORIZED)
        payload = JWTAppManager.decode_token(token)
        user_id = payload.get('uid')
        verify_token = Authentication.verify_token(token)
        if verify_token is None:
            return Authentication.construct_response('Token invalid or expired!!!', None, StatusCode.HTTP_FORBIDDEN)
        user_info = Users.get_user(id=user_id)
        result = Authentication.copy_dict(user_info.to_dict(), ["email", "fullname", "username"])
        return Authentication.construct_response('success', result, StatusCode.HTTP_OK, verify_token)

    @staticmethod
    def get_all_user():
        token = request.headers.get('XSRF-Token', None)
        if token is None:
            return Authentication.construct_response('Haven\'t access token', None, StatusCode.HTTP_UNAUTHORIZED)
        verify_token = Authentication.verify_token(token)
        if verify_token is None:
            return Authentication.construct_response('Token invalid or expired!!!', None, StatusCode.HTTP_FORBIDDEN)
        user_info = Users.get_all_user()
        all_data = [
            {k: v for k, v in users.to_dict().items() if k not in ['id', 'ref_token', 'password']} for
            users in user_info]
        return Authentication.construct_response('success', all_data, StatusCode.HTTP_OK, verify_token)

    @staticmethod
    def delete_user():
        data = request.json
        validate = Validator(username_schema)
        if not validate.validate(data):
            return Authentication.construct_response('Validation Error', validate.errors, StatusCode.HTTP_BAD_REQUEST)
        username = data.get('username', None)
        user = Users.get_user(username=username)
        if user is None:
            return Authentication.construct_response('User not found', None, StatusCode.HTTP_NOT_FOUND)

        token = request.headers.get('XSRF-Token', None)
        if token is None:
            return Authentication.construct_response('Haven\'t access token', None, StatusCode.HTTP_UNAUTHORIZED)

        verify_token = Authentication.verify_token(token)
        if verify_token is None:
            return Authentication.construct_response('Token invalid or expired!!!', None, StatusCode.HTTP_FORBIDDEN)

        delete_info = Users.delete_user(user.id)
        if delete_info is not None:
            message = f'User {delete_info} has been deleted!'
        else:
            message = f'Delete user have error!'
        return Authentication.construct_response(message, None, StatusCode.HTTP_OK, verify_token)

    @staticmethod
    def forget_password():
        data = request.json
        validate = Validator(username_schema)
        if not validate.validate(data):
            return Authentication.construct_response('Validation Error', validate.errors, StatusCode.HTTP_BAD_REQUEST)

        username = data.get('username', None)
        user = Users.get_user(username=username)
        if user is None:
            return Authentication.construct_response('User not found', None, StatusCode.HTTP_NOT_FOUND)
        sender_email = Config.MAIL_USERNAME
        receiver_email = user.email

        token = JWTAppManager.create_access_token(user.id, expired_in_minutes=5)
        if token:
            subject = 'Reset Password Token'
            body = f'Hello {user.fullname},\n\nHere is your reset password token have expired on 5 minutes: {token}'
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = receiver_email

            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_username = sender_email
            smtp_password = 'tbqe ogdb wksb mdap'
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, [receiver_email], msg.as_string())
            server.quit()
            return Authentication.construct_response('success',
                                                     "Please check your email and send request to reset your password !",
                                                     StatusCode.HTTP_OK)

    @staticmethod
    def set_password():
        data = request.json
        validate = Validator(password_schema)
        if not validate.validate(data):
            return Authentication.construct_response('Validation Error', validate.errors, StatusCode.HTTP_BAD_REQUEST)

        password = data.get('password', None)
        token = request.headers.get('XSRF-Token', None)
        if token is None:
            return Authentication.construct_response('Haven\'t reset password token', None,
                                                     StatusCode.HTTP_UNAUTHORIZED)
        payload = JWTAppManager.decode_token(token)
        user_id = payload.get('uid')
        expired_time = payload.get('exp')

        if datetime.utcfromtimestamp(expired_time) < datetime.utcnow():
            return Authentication.construct_response('Expired token', None, StatusCode.HTTP_UNAUTHORIZED)

        user = Users.get_user(id=user_id)
        if user is None:
            return Authentication.construct_response('User not exist', None, StatusCode.HTTP_NOT_FOUND)
        update_password = Users.update(user_id, password=password)
        user_info = Authentication.copy_dict(user.to_dict(), ["email", "fullname", "username"])
        user_info['password'] = update_password

        create_token = Users.save_new_token(user_id)
        if create_token is None:
            return Authentication.construct_response("error", "Update token is error", StatusCode.HTTP_UNAUTHORIZED)
        token = create_token.json
        user_info['access_token'] = token.get('access_token', None)
        return Authentication.construct_response('success', user_info, StatusCode.HTTP_OK)

    @staticmethod
    def verify_token(token):
        payload = JWTAppManager.decode_token(token)
        user_id = payload.get('uid')
        expired_time = payload.get('exp')
        if datetime.utcfromtimestamp(expired_time) > datetime.utcnow() is True:
            return token
        user_info = Users.get_user(id=user_id)
        if user_info is None:
            return None
        refresh_token = user_info.ref_token
        payload_refresh = JWTAppManager.decode_token(refresh_token)
        expired_refresh = payload_refresh.get('exp')
        if datetime.utcfromtimestamp(expired_refresh) < datetime.utcnow() is True:
            return None
        new_token = JWTAppManager.create_access_token(user_id)
        return new_token

    @staticmethod
    def copy_dict(source_dict, keys, exclude=False):
        try:
            if exclude:
                result = {key: value for key, value in source_dict.items() if key not in keys}
            else:
                result = {key: source_dict[key] for key in keys if key in source_dict}
            return result
        except Exception as e:
            return {}
