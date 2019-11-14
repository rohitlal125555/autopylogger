import os
import logging
import traceback
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


def prepare_log_directory(log_name, log_directory):
    """

    Function to prepare directory structure

    :return: Path of log directory
    :rtype: str

    """
    try:
        base_logs_path = log_directory
        if not os.path.exists(base_logs_path):
            os.mkdir(base_logs_path)

        logs_file_path = os.path.join(base_logs_path, log_name)

        # print("Log Path : %s" % str(logs_file_path))

        if not os.path.exists(logs_file_path):
            # print("Making directory : %s" % str(logs_file_path))
            os.mkdir(logs_file_path)

        if not os.path.exists(os.path.join(logs_file_path, 'Error')):
            os.mkdir(os.path.join(logs_file_path, 'Error'))

        if not os.path.exists(os.path.join(logs_file_path, 'Debug')):
            os.mkdir(os.path.join(logs_file_path, 'Debug'))

        if not os.path.exists(os.path.join(logs_file_path, 'Info')):
            os.mkdir(os.path.join(logs_file_path, 'Info'))

        if not os.path.exists(os.path.join(logs_file_path, 'Warning')):
            os.mkdir(os.path.join(logs_file_path, 'Warning'))

        return logs_file_path

    except Exception:
        exception_message = traceback.format_exc()
        raise NotADirectoryError('Unable to make logging directory structure. Details: %s' % str(exception_message))


def help():
    """

    Helper function for using the logging module.

    Call this function to print the example usage of module on the console.

    :return: None

    """
    print("\n------------------------------------------------------------------------------------------", end='')
    print("--------------------------------------------------------------------------------------------")
    print("\n\t Welcome to the python log rotate module! ")
    print("\n------------------------------------------------------------------------------------------", end='')
    print("--------------------------------------------------------------------------------------------")

    print("\nThis is a generic logging wrapper built on python logging library with "
          "log rotation feature built in.")

    print("Function definition")
    print("\ninit_logging(log_name, log_directory, log_mode, max_bytes, rotate_when, rotate_interval, "
          "backup_count, encoding, delay, log_level, console_log, rotation_criteria, log_format)")

    print("\n USAGE :")
    print("\nStep 1: Initialize your logger object by calling the 'init_logging' function")
    print("\n\t\tfrom python_log_rotate import init_logging")
    print("\n\t\tmy_logger_obj = init_logging(log_name='my_logs', log_directory='logs_dir')")

    print("\nStep 2: Usage the object for writing DEBUG|INFO|WARNING|ERROR logs")
    print("\n\t\tmy_logger_obj.debug('This is DEBUG log')")
    print("\n\t\tmy_logger_obj.info('This is INFO log')")
    print("\n\t\tmy_logger_obj.warning('This is WARNING log')")
    print("\n\t\tmy_logger_obj.error('This is ERROR log')")


def init_logging(log_name='logger', log_directory='logs', log_mode='a', max_bytes=100 * 1024 * 1024, rotate_when='d',
                 rotate_interval=1, backup_count=20, encoding=None, delay=0, log_level=logging.INFO, console_log=True,
                 rotation_criteria='size',
                 log_format='[%(asctime)s] -- %(levelname)s - %(filename)s -- %(funcName)s - Line no - %(lineno)d -- '
                            '%(message)s\n'):
    """

    Function to initialize logging library with log rotation feature enabled.

    Please note, arguments related to log rotation depends on the chosen rotation criteria.

    For rotation criteria == 'size', 'log_mode' & 'max_bytes' are required.
    For rotation criteria == 'time', 'rotate_when' & 'rotate_interval' are required

    :param log_name: Name of log
    :type log_name: str
    :param log_directory: Directory for saving log files
    :type log_directory: str
    :param log_mode: Mode of logging. Options: Append('a') | Write ('w')
    :type log_mode: str
    :param max_bytes: Max file size
    :type max_bytes: int
    :param rotate_when: When to rotate. Options: day('d') | hour('h') | minute('m') | seconds('s')
    :type rotate_when: str
    :param rotate_interval: Interval for rotation
    :type rotate_interval: int
    :param backup_count: Number of backup files to keep on rotation
    :type backup_count: int
    :param encoding: Encoding scheme for logging
    :type encoding: str
    :param delay: Delay flag for logging.
    :type delay: int
    :param log_level: Log level
    :type log_level: int
    :param console_log: Flag for turning console logging on or off.
    :type console_log: Boolean
    :param rotation_criteria: Type of rotation. Options: 'size' | 'time'
    :type rotation_criteria: str
    :param log_format: Log formatter for setting log pattern
    :type log_format: str
    :return: Logger object
    :rtype: Logger

    """

    try:
        logs_path = prepare_log_directory(log_name=log_name, log_directory=log_directory)

        log = logging.getLogger(log_name)
        log_formatter = logging.Formatter(log_format)

        # Adding log handler for logging on console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)

        # Variables for log paths for DEBUG, INFO, WARN, ERROR
        debug_log_file_name = os.path.join(os.path.join(logs_path, 'Debug'), (log_name + '.debug'))
        info_log_file_name = os.path.join(os.path.join(logs_path, 'Info'), (log_name + '.info'))
        warning_log_file_name = os.path.join(os.path.join(logs_path, 'Warning'), (log_name + '.warn'))
        error_log_file_name = os.path.join(os.path.join(logs_path, 'Error'), (log_name + '.error'))

        if rotation_criteria.lower() == 'size':
            # Log handlers for size based file rotation
            debug_file_handler = RotatingFileHandler(debug_log_file_name, mode=log_mode, maxBytes=max_bytes,
                                                     backupCount=backup_count, encoding=encoding, delay=delay)
            info_file_handler = RotatingFileHandler(info_log_file_name, mode=log_mode, maxBytes=max_bytes,
                                                    backupCount=backup_count, encoding=encoding, delay=delay)
            warning_file_handler = RotatingFileHandler(warning_log_file_name, mode=log_mode, maxBytes=max_bytes,
                                                       backupCount=backup_count, encoding=encoding, delay=delay)
            error_file_handler = RotatingFileHandler(error_log_file_name, mode=log_mode, maxBytes=max_bytes,
                                                     backupCount=backup_count, encoding=encoding, delay=delay)
        else:
            # Log handlers for time based file rotation
            debug_file_handler = TimedRotatingFileHandler(debug_log_file_name, when=rotate_when,
                                                          interval=rotate_interval, backupCount=backup_count,
                                                          encoding=encoding, delay=delay)
            info_file_handler = TimedRotatingFileHandler(info_log_file_name, when=rotate_when,
                                                         interval=rotate_interval, backupCount=backup_count,
                                                         encoding=encoding, delay=delay)
            warning_file_handler = TimedRotatingFileHandler(warning_log_file_name, when=rotate_when,
                                                            interval=rotate_interval, backupCount=backup_count,
                                                            encoding=encoding, delay=delay)
            error_file_handler = TimedRotatingFileHandler(error_log_file_name, when=rotate_when,
                                                          interval=rotate_interval, backupCount=backup_count,
                                                          encoding=encoding, delay=delay)

        # Setting log handler properties
        debug_file_handler.setFormatter(log_formatter)
        debug_file_handler.setLevel(logging.DEBUG)
        debug_file_handler.addFilter(MyFilter(logging.DEBUG))

        info_file_handler.setFormatter(log_formatter)
        info_file_handler.setLevel(logging.INFO)
        info_file_handler.addFilter(MyFilter(logging.INFO))

        warning_file_handler.setFormatter(log_formatter)
        warning_file_handler.setLevel(logging.WARNING)
        warning_file_handler.addFilter(MyFilter(logging.WARNING))

        error_file_handler.setFormatter(log_formatter)
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.addFilter(MyFilter(logging.ERROR))

        # Adding log handlers to the log object if not already added
        # Checking is performed to prevent any duplicate addition of handlers
        if not len(log.handlers):

            if console_log:
                log.addHandler(stream_handler)

            log.addHandler(debug_file_handler)
            log.addHandler(info_file_handler)
            log.addHandler(warning_file_handler)
            log.addHandler(error_file_handler)

        # Setting log level
        log.setLevel(log_level)

        return log

    except Exception:
        exception_message = traceback.format_exc()
        raise Exception('Error occurred in setting up logging. Details: %s' % str(exception_message))


class MyFilter(object):
    def __init__(self, level):
        self.__level = level

    def filter(self, log_record):
        return log_record.levelno <= self.__level
