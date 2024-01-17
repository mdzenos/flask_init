import re
from flask import jsonify
from app.models import db

from .status_code import StatusCode
from .error_code import ErrorCode

from common.constant import RESPONSE_DESCRIPTION
from common.error_code import ERROR_MESSAGE

from sqlalchemy.exc import SQLAlchemyError
from jwt.exceptions import PyJWTError
from werkzeug.exceptions import MethodNotAllowed

class APIException(Exception):
    status_code = StatusCode.HTTP_INTERNAL_SERVER_ERROR
    error_code = 'default'

    def __init__(self, message=None, error_code=None, description=None):
        super().__init__()
        self.message = message or "Error"
        self.error_code = error_code or self.error_code
        self.description = description

    def get_response(self):
        response = {
            'response': {
                'message': ERROR_MESSAGE.get(self.error_code, None),
                'code': self.error_code,
                'result': self.description
            }
        }
        return jsonify(response)

class BadRequest(APIException):
    status_code = StatusCode.HTTP_BAD_REQUEST
    error_code = ErrorCode.VALIDATION_ERROR


class CustomBadRequest(BadRequest):
    status_code = StatusCode.HTTP_BAD_REQUEST
    error_code = ErrorCode.VALIDATION_ERROR
    description_code = 1000


class Unauthorized(APIException):
    status_code = StatusCode.HTTP_UNAUTHORIZED
    error_code = ErrorCode.IDENTIFICATION_CONFIRMATION_FAILED
    description_code = 401


class NotFound(APIException):
    status_code = StatusCode.HTTP_NOT_FOUND
    description_code = 404

class DatabaseException(APIException):
    def __init__(self, error: SQLAlchemyError):
        self.message = None
        self.code = None
        self.description = None

        if hasattr(error, 'code'):
            self.code = error.code
        if hasattr(error, '_message') and callable(getattr(error, '_message')):
            error_message = str(error._message())

            match_message = re.search(r'\((?:[^.)]+\.){1}([^).]+)\)', error_message)
            if match_message:
                message = match_message.group(1)
                match message:
                    case "IntegrityError":
                        self.code = ErrorCode.INTEGRITY_ERROR
                    case "NoResultFound":
                        self.code = ErrorCode.NO_RESULT_FOUND
                    case "MultipleResultsFound":
                        self.code = ErrorCode.MULTIPLE_RESULTS_FOUND
                    case "InvalidRequestError":
                        self.code = ErrorCode.INVALID_REQUEST_ERROR
                    case "DataError":
                        self.code = ErrorCode.DATA_ERROR
                    case "OperationalError":
                        self.code = ErrorCode.OPERATIONAL_ERROR

            match_description = re.search(r'\"(.+?)\"', error_message)
            if match_description:
                self.description = match_description.group(1)
            if "Duplicate entry" in self.description:
                start_index = error_message.find("for key '") + len("for key '")
                end_index = error_message.find("'", start_index)
                description = None
                field = []
                if start_index != -1 and end_index != -1:
                    description = error_message[start_index:end_index].split('.')
                if len(description) > 1:
                    field = description[1]
                if len(field) > 0:
                    self.description = field.capitalize() + " is exist"

        super().__init__(message=self.message, error_code=self.code, description=self.description)

class JWTException(Unauthorized):
    def __init__(self, error: PyJWTError):
        self.message = "Token error"
        self.code = None
        self.description = error

        if "Invalid header string" in error:
            self.code = ErrorCode.DECODE_TOKEN_ERROR
        super().__init__(message=self.message, error_code=self.code, description=self.description)

class IllegalIpAddress(Unauthorized):
    error_code = ErrorCode.ILLEGAL_IP_ADDRESS
    description_code = 40003

class AttributeException(APIException):
    error_code = 'A00001'
    def __init__(self, error: Exception):
        self.description = str(error)
        super().__init__(description=self.description)

def handle_exception(error):
    error.status_code = StatusCode.HTTP_INTERNAL_SERVER_ERROR
    if isinstance(error, AttributeError) or isinstance(error, TypeError):
        error = AttributeException(error)
    # elif isinstance(error, MethodNotAllowed):
    #     error = MethodException(error)
    elif isinstance(error, PyJWTError):
        error = JWTException(error)
    elif not isinstance(error, Exception):
        error = APIException()
    elif isinstance(error, SQLAlchemyError):
        db.session.rollback()
        error = DatabaseException(error)
    return error.get_response(), error.status_code
