
username_schema = {
    'username': {'type': 'string', 'minlength': 3, 'maxlength': 20, 'required': True}
}

password_schema = {
    'password': {'type': 'string', 'minlength': 6, 'required': True},
}

user_password_schema = {
    'old_password': {'type': 'string', 'minlength': 6, 'required': True},
    'new_password': {'type': 'string', 'minlength': 6, 'required': True}
}

user_registration_schema = {
    'fullname': {'type': 'string', 'minlength': 3, 'maxlength': 20},
    'username': {'type': 'string', 'minlength': 3, 'maxlength': 20, 'required': True},
    'password': {'type': 'string', 'minlength': 6, 'required': True},
    'email': {'type': 'string', 'maxlength': 30,'required': True, 'regex': r'\S+@\S+\.\S+'}
}

user_login_schema = {
    'username': {'type': 'string', 'minlength': 3, 'maxlength': 20, 'required': True},
    'password': {'type': 'string', 'minlength': 6, 'required': True}
}

RESPONSE_DESCRIPTION = {
    1000: 'No data needed from client',
    500: 'Internal Server Error',
    401: 'Unauthorized',
    404: 'Not Found',
    40001: 'Missing CSRF-TOKEN',
    40002: 'Token not exist in database',
    40003: 'Illegal ip address'
}

API_V1_PREFIX = '/api/v1'
API_V2_PREFIX = '/api/v2'