import jwt
import hashlib
from config import Config
from datetime import datetime, timedelta


class PassWordManager:
    def hash_password(password):
        algorithm = 'sha256'
        salt = Config.SECURITY_PASSWORD_SALT
        salt = salt.encode('utf-8')

        hasher = hashlib.new(algorithm)

        hasher.update(salt)
        hasher.update(password.encode('utf-8'))

        return hasher.hexdigest()

    def check_password(password, hashed_password):
        salt = Config.SECURITY_PASSWORD_SALT

        salt = salt.encode('utf-8')

        hasher = hashlib.new('sha256')

        hasher.update(salt)
        hasher.update(password.encode('utf-8'))

        input_hashed_password = hasher.hexdigest()

        return hashed_password == input_hashed_password


class JWTManager:

    @staticmethod
    def create_token(user_id, expired_in_minutes=30):
        try:
            expiration_time = datetime.utcnow() + timedelta(minutes=expired_in_minutes)
            payload = {
                'uid': user_id,
                'exp': expiration_time
            }
            secret_key = Config.SECRET_KEY
            return jwt.encode(payload=payload, key=secret_key, algorithm='HS256').decode('utf-8')
        except Exception as e:
            print(f"Error creating token: {e}")
            return None

    @staticmethod
    def decode_token(token):
        try:
            secret_key = Config.SECRET_KEY
            decoded_payload = jwt.decode(jwt=token, key=secret_key, algorithms=['HS256'])
            return decoded_payload
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
            return None
        except jwt.InvalidTokenError:
            print("Invalid token.")
            return None
        except Exception as e:
            print(f"Error decoding token: {e}")
            return None