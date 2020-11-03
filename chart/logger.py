#!/usr/bin/python
#
# Copyright 2020 Kingston Technology Far East Co. Ltd. All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Edwin Lai <Edwin_Lai@kingston.com.tw>, March 2020

"""The Logger module provide different type of handler.

Implement log filter and thread swapping.
Provide different type of handler include file, ui and console logger.
"""

import logging.config
import os
import sys
import threading
from logging import StreamHandler

logger_lock = threading.Lock()


class RootLoggingFilter(logging.Filter):
    def filter(self, record):
        thread_name = threading.current_thread().name

        logger = logging.getLogger('root.report')
        original_name = thread_name

        logger.propagate = False
        if hasattr(record, 'asctime'):
            msg = '[{}][{}][{}] - {}'.format(record.asctime, record.levelname,
                                             thread_name, record.msg)
        else:
            record.threadNmae = thread_name
            msg = record.msg
        logger.log(record.levelno, msg, *record.args)
        if record.levelno >= logging.getLevelName('ERROR') and record.exc_text:
            logger.log(record.levelno, record.exc_text)
        logger.propagate = True
        logging.getLogger('root')
        threading.current_thread().name = original_name
        return True


def setup_loggers(start_time, prefix='', filename=''):
    """Setup logger for all the process, including MainProcess.
    Args:
      start_time: The log create time.
      prefix: prefix directory of the log file.
      filename: log file name.
    Returns:
      file_name: The log abs. filename.
    Raises:
      None
    """
    with logger_lock:
        term = sys.stdout

        if not logging.getLogger().handlers[0].name:
            config = {
                'version': 1,
                'filters': {
                    'RootLoggingFilter': {
                        '()': RootLoggingFilter
                    },
                },
                'formatters': {
                    'standard_formatter': {
                        'format': '[%(asctime)s][%(levelname)6s]'
                                  '[%(threadName)7s] - %(message)s',
                        'datefmt': '%Y-%m-%d %H:%M:%S'
                    },
                },
                'handlers': {
                    'console_handler': {
                        'class': 'logging.StreamHandler',
                        'level': logging.DEBUG,
                        'formatter': 'standard_formatter',
                        'stream': term,
                        'filters': ['RootLoggingFilter']
                    },
                },
                'root': {
                    'level': logging.DEBUG,
                    'handlers': ['console_handler']
                },
            }
            logging.config.dictConfig(config)

    if prefix and not os.path.isdir(prefix):
        os.makedirs(prefix, exist_ok=True, mode=0o777)

    if not filename:
        file_name = 'report_{}.log'.format(start_time)
    else:
        file_name = '{}/{}'.format(prefix, filename)

    handler = logging.FileHandler(file_name)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s]'
                                  '[%(threadName)7s] - %(message)s',
                                  '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    slot_logger = logging.getLogger('root.report')
    slot_logger.handlers = []
    slot_logger.addHandler(handler)

    return file_name


def add_text_handler(callback=None):
    """Add TextHandler to specific logger, to output log messages to user
    interface."""
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s]'
                                  '[%(threadName)7s] - %(message)s',
                                  '%Y-%m-%d %H:%M:%S')
    slot_logger = logging.getLogger('root.report')

    text_handler = TextHandler(callback)
    text_handler.setFormatter(formatter)
    text_handler.setLevel(logging.DEBUG)
    slot_logger.addHandler(text_handler)


class TextHandler(logging.StreamHandler):
    """Log handler output to QTextEdit in MainWindow, through
    callback function."""
    def __init__(self, callback=None):
        StreamHandler.__init__(self, stream=None)
        self._callback = callback

    def emit(self, record):
        if self._callback:
            msg = self.format(record)
            self._callback(str(msg.encode('utf-8')))
