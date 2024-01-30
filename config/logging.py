import os
import logging
from logging.handlers import TimedRotatingFileHandler
from common.constant import LOG_LEVEL
from datetime import datetime


class Log:
    @staticmethod
    def write(package=__package__, level='info', message: str = '', request=None):
        package_name = package.split('.')[1]
        ip_address = request.remote_addr if request is not None else '127.0.0.1'
        Log.setup(package_name)
        logger = logging.getLogger(package_name)
        message = f'{ip_address}: {message}'
        getattr(logger, level)(str(message))

    @staticmethod
    def setup(package_name):
        if not logging.getLogger(package_name).handlers:
            logging.basicConfig(level=logging.DEBUG)
            log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
            date_log_dir = os.path.join(log_dir, datetime.utcnow().strftime('%Y-%m-%d'))

            os.makedirs(log_dir, exist_ok=True)
            os.makedirs(date_log_dir, exist_ok=True)

            formatter = logging.Formatter('%(asctime)s: [%(levelname)s] - %(message)s')

            module_logger = logging.getLogger(package_name)
            module_log_path = os.path.join(date_log_dir, f'{package_name}.log')

            if not any(isinstance(handler, TimedRotatingFileHandler) for handler in module_logger.handlers):
                module_handler = TimedRotatingFileHandler(module_log_path, when='midnight', interval=1, backupCount=7,
                                                          encoding='utf-8')
                module_handler.setLevel(logging.DEBUG)
                module_handler.setFormatter(formatter)
                module_logger.addHandler(module_handler)
