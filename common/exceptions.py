from common.status_code import StatusCode
from common.error_code import ErrorCode, ERROR_MESSAGE
from flask import jsonify

class CustomException(Exception):
    status_code = StatusCode.HTTP_INTERNAL_SERVER_ERROR
    def __init__(self, status_code=None, message=None, description=None, error_code=None):
        super().__init__()
        self.status_code = status_code or self.status_code
        self.error_code = error_code
        self.message = message
        if error_code is None and message is None:
            self.error_code = self.status_code
        self.description = description

    def get_response(self):
        response = {
            'error': {
                'code': self.error_code,
                'message': self.message or ERROR_MESSAGE.get(self.error_code, ''),
                'description': self.description
            }
        }
        return jsonify(response)


class AttributeException(CustomException):
    def __init__(self, error: Exception):
        self.status_code = StatusCode.HTTP_INTERNAL_SERVER_ERROR
        self.error_code = ErrorCode.ATTRIBUTE_TYPE_ERROR
        self.message = ERROR_MESSAGE.get(self.error_code, '')
        self.description = str(error)
        super().__init__(status_code=self.status_code, message=self.message, description=self.description, error_code=self.error_code)


def handle_exception(error):
    if isinstance(error, AttributeError) or isinstance(error, TypeError):
        print(1)
        response = {
            'error': {
                'code': 'ATTRIBUTE_ERROR_OR_TYPE_ERROR',
                'description': 'Attribute error or type error occurred',
                'message': str(error)
            }
        }
        return jsonify(response), StatusCode.HTTP_INTERNAL_SERVER_ERROR
    elif isinstance(error, AttributeError) or isinstance(error, TypeError):
        error = AttributeException(error)
    return error.get_response(), error.status_code