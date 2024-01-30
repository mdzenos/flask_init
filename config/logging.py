import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

def setup_logger(module_name):
    logging.basicConfig(level=logging.DEBUG)

    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
    date_log_dir = os.path.join(log_dir, datetime.utcnow().strftime('%Y-%m-%d'))

    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(date_log_dir, exist_ok=True)

    formatter = logging.Formatter('%(asctime)s:(%(module)s) - %(levelname)s: %(message)s')

    module_logger = logging.getLogger(module_name)
    module_log_path = os.path.join(date_log_dir, f'{module_name}.log')
    module_handler = TimedRotatingFileHandler(module_log_path, when='midnight', interval=1, backupCount=7, encoding='utf-8')
    module_handler.setLevel(logging.DEBUG)
    module_handler.setFormatter(formatter)
    module_logger.addHandler(module_handler)