import logging
import os
from logging.handlers import RotatingFileHandler

log_dir_name = os.path.dirname(os.path.realpath(__file__))


def create_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(
        os.path.join(log_dir_name, f'{name}.log'),
        encoding='UTF-8',
        maxBytes=2000,
        backupCount=10,
    )
    formatter = logging.Formatter(
        '%(name)s %(asctime)s %(levelname)s %(message)s',
        datefmt='%d-%b-%y %H:%M:%S',
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
