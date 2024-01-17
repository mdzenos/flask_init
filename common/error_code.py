class ErrorCode:
    RECAPTCHA_RESPONSE_ERROR = "E00001"
    PRESCRIPTION_DELIVER_SERVICE_FAILED = "E00002"
    TOKEN_NOT_EXIST_IN_DATABASE = "E00003"
    FAILED_TO_CREATE_ACCESS_TOKEN = "E00004"
    SYSTEM_ERROR = "E00005"
    ACCESS_KEY_EXISTED = "E00006"
    ILLEGAL_IP_ADDRESS = "E00007"
    QUESTIONNAIRE_NOT_EXIST = "W00001"
    IDENTIFICATION_CONFIRMATION_FAILED = "W00002"
    IDENTIFICATION_CONFIRMATION_FAILED_MULTIPLE_TIMES = "W00003"
    IDENTIFICATION_CONFIRMATION_URL_EXPIRED = "W00004"
    ACCESS_TOKEN_EXPIRED = "W00005"
    RECAPTCHA_SCORE_LOWER_THAN_DEFAULT = "W00006"
    VALIDATION_ERROR = "W00007"
    PHYSICAL_DELETE_INFO = "I00001"
    PHYSICAL_DELETE_COUNT = "I00002"
    PHYSICAL_ACCESS_TOKEN_DELETE_COUNT = "I00003"
    ATTRIBUTE_TYPE_ERROR = "A00001"
    USER_EXIST = "U00001"
    INTEGRITY_ERROR = "D00001"
    NO_RESULT_FOUND = "D00002"
    MULTIPLE_RESULTS_FOUND = "D00003"
    INVALID_REQUEST_ERROR = "D00004"
    DATA_ERROR = "D00005"
    OPERATIONAL_ERROR = "D00006"
    DECODE_TOKEN_ERROR = "J00001"

ERROR_MESSAGE = {
    "E00001": "reCAPTCHA response error",
    "E00002": "Prescription deliver service failed",
    "E00003": "Token not exist in data base",
    "E00004": "Failed to create access token",
    "E00005": "System error",
    "E00006": "Access key existed",
    "E00007": "Illegal ip address",
    "W00001": "Questionnaire not exists",
    "W00002": "Identification confirmation failed",
    "W00003": "Identification confirmation failed multiple times",
    "W00004": "Identification confirmation url expired",
    "W00005": "Access token expired",
    "W00006": "reCaptcha score lower than default",
    "W00007": "Validation error",
    "I00001": "Physical delete information",
    "I00002": "Physical delete count",
    "I00003": "Physical access token delete count",
    "A00001": "Attribute error or type error occurred",
    "D00001": "Lỗi toàn vẹn dữ liệu",
    "D00002": "Không có dữ liệu",
    "D00003": "Tìm thấy nhiều dữ liệu",
    "D00004": "Yêu cầu không hợp lệ",
    "D00005": "Kiểu dữ liệu hợp lệ",
    "D00006": "Lỗi thực thi",
    "J00001": "Can't decode your token"
}
