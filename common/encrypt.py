import hashlib

from common.exceptions import JWTException
from config.database import Config
from datetime import datetime, timedelta
import jwt
from jwt import PyJWTError


class PassWordManager:

    @staticmethod
    def hash_password(password):
        algorithm = 'sha256'
        salt = Config.SECURITY_PASSWORD_SALT
        salt = salt.encode('utf-8')

        hasher = hashlib.new(algorithm)

        hasher.update(salt)
        hasher.update(password.encode('utf-8'))

        return hasher.hexdigest()

    @staticmethod
    def check_password(password, hashed_password):
        salt = Config.SECURITY_PASSWORD_SALT

        salt = salt.encode('utf-8')
        hasher = hashlib.new('sha256')

        hasher.update(salt)
        hasher.update(password.encode('utf-8'))

        input_hashed_password = hasher.hexdigest()

        return hashed_password == input_hashed_password


class JWTAppManager:

    @staticmethod
    def create_access_token(user_id, expired_in_minutes=60):
        try:
            expiration_time = datetime.utcnow() + timedelta(minutes=expired_in_minutes)
            payload = {
                'uid': user_id,
                'exp': expiration_time
            }
            secret_key = Config.SECRET_KEY
            return jwt.encode(payload=payload, key=secret_key, algorithm='HS256')
        except PyJWTError as e:
            raise JWTException(str(e))
        except Exception as e:
            return str(e)

    @staticmethod
    def create_refresh_token(user_id, expired_in_days=10):
        try:
            expiration_time = datetime.utcnow() + timedelta(days=expired_in_days)
            payload = {
                'uid': user_id,
                'exp': expiration_time
            }
            secret_key = Config.SECRET_KEY
            return jwt.encode(payload=payload, key=secret_key, algorithm='HS256')
        except PyJWTError as e:
            raise JWTException(str(e))
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        try:
            secret_key = Config.SECRET_KEY
            decoded_payload = jwt.decode(jwt=token, key=secret_key, algorithms=['HS256'], options={'verify_exp': False})#
            return decoded_payload
        except PyJWTError as e:
            raise JWTException(str(e))
        except Exception as e:
            return e
