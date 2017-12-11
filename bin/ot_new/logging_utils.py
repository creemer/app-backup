# coding=utf-8

from logging import Formatter
from logging.handlers import RotatingFileHandler


class LoggingUtils:
    def __init__(self):
        pass

    @staticmethod
    def create_default_fh(filepath, formatter=None, max_part_mb=5, max_parts_count=9):
        fh = RotatingFileHandler(
            filename=filepath,
            encoding='utf-8',
            mode='a',
            maxBytes=max_part_mb * 1024 * 1024,
            backupCount=max_parts_count
        )
        if formatter is not None:
            fh.setFormatter(formatter)
        return fh

    @staticmethod
    def default_log_formatter():
        return Formatter('%(asctime)s %(levelname)-8s %(message)s')
