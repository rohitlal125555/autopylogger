import os
import logging
import traceback
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler, SMTPHandler
import time
import smtplib
import warnings
warnings.simplefilter('always', DeprecationWarning)


class SizedTimedRotatingFileHandler(TimedRotatingFileHandler):
    """
    Handler for logging to a set of files, which switches from one file
    to the next when the current file reaches a certain size, or at certain
    timed intervals
    """

    def __init__(self, filename, maxBytes=0, backupCount=0, encoding=None,
                 delay=0, when='h', interval=1, utc=False):
        TimedRotatingFileHandler.__init__(
            self, filename, when, interval, backupCount, encoding, delay, utc)
        self.maxBytes = maxBytes

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        Basically, see if the supplied record would cause the file to exceed
        the size limit we have.
        """

        # Size based rotation condition
        if self.stream is None:                 # delay was set...
            self.stream = self._open()
        if self.maxBytes > 0:                   # are we rolling over?
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)  # due to non-posix-compliant Windows feature
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1

        # Time based rotation condition
        t = int(time.time())
        if t >= self.rolloverAt:
            return 1
        return 0


class MyFilter(object):
    def __init__(self, level):
        self.__level = level

    def filter(self, log_record):
        return log_record.levelno <= self.__level


class ExperimentalFeatureWarning(Warning):
    pass


class ArgumentError(Exception):

    # Constructor or Initializer
    def __init__(self, value):
        self.value = value

    # __str__ is to print() the value
    def __str__(self):
        return repr(self.value)


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

    print(
        """

Python thread-safe logging wrapper module with out of box log rotation and critical logs mailing facility built 
for seamless integration in any python script.

Requirements: logging

#### Basic Usage :

- Initialize your logger object by calling the 'init_logging' function *(with mailing feature turned OFF)*

        from autopylogger import init_logging
        my_logger_obj = init_logging(log_name='my_logs', log_directory='logs_dir')

- Initialize your logger object by calling the 'init_logging' function *(with mailing feature turned ON)*

        from autopylogger import init_logging
        my_logger_obj = init_logging(log_name='my_logs', log_directory='logs_dir', enable_mailing=True, 
                                    mail_host='mymail.host.com', mailfrom_addr='<email_address>', 
                                    mailto_addr='<email_address>', mail_subject='<subject>', 
                                    mail_credentials=('<username>', '<password>'))

- Use the object for writing DEBUG|INFO|WARNING|ERROR logs

        my_logger_obj.debug('This is DEBUG log')
        my_logger_obj.info('This is INFO log')
        my_logger_obj.warning('This is WARNING log')
        my_logger_obj.error('This is ERROR log')
        my_logger_obj.critical('This is CRITICAL log. Mail will be sent with this message')

### Important Flags:

- **Setting log level:** *Pass the appropriate value to the **"log_level"** flag.*

        log_level = 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR'

- **Turning console logging ON/OFF:** *Pass the appropriate vlaue to the **"console_log"** flag.*

        console_log = True | False

- **Setting log rotation criteria:** *Pass the appropriate value to the **"rotation_criteria"** flag.*

        rotation_criteria = 'size' | 'time' | 'timeandsize'

  By default, rotation criteria **"size"** is used with max file size of 200 Mbs.
  
  - When choosing 'size' based rotation criteria, pass the argument value **'max_bytes'** to specify the max size 
        of log file in bytes.

        'rotation_criteria' = 'size'
        'max_bytes' = 5*1024*1024

  - When choosing **"time"** based rotation criteria, pass the argument value **"rotate_when"** & **"rotate_interval"**.

        'rotation_criteria' = 'time'
        'rotate_when' = 'd' | 'h' | 'm' | 's'
        'rotate_interval' = 1 (for rotating log every 1 day|hour|minute|second)
  
  - When choosing **"timeandsize"** based rotation criteria, pass the argument value **"rotate_when"**, 
                **"rotate_interval"** & **'max_bytes'**.

        'rotation_criteria' = 'timeandsize'
        'max_bytes' = 5*1024*1024
        'rotate_when' = 'd' | 'h' | 'm' | 's'
        'rotate_interval' = 1 (for rotating log every 1 day|hour|minute|second)
        
  *NOTE: In "timeandsize" rotation criteria, a file is rotate when either of the time or size constraint 
        gets satisfied."*
  
  
- **Turning critical mailing ON/OFF:** *Pass the boolean value (TRUE|FALSE) to the **"enable_mailing"** flag. 
        By default mailing is enabled for critical errors.*
   
  - When **"enable_mailing"** is set to True, following flags are required. 

        'mail_host' = '<Mail host name / ip address>'
        'mailfrom_addr' = '<Sender email address>'
        'mailto_addr' = '<Receiver email address>'
        'mail_subject' = '<Mail subject>'
        'mail_credentials' = ('<username>', '<password>')
  

- **Setting log format:** *Pass the desired log format string to the **"log_format"** flag*

        log_format='[%(asctime)s] -- %(levelname)s - %(filename)s -- %(funcName)s - Line no - %(lineno)d -- %(message)s'

##### Log formatter arguments:
   
| Format | Description |
| ------ | ------ |
| %(asctime)s | Human-readable time when the LogRecord was created. |
| %(created)f | Time when the LogRecord was created (as returned by time.time()). |
| %(filename)s | Filename portion of pathname. |
| %(funcName)s | Name of function containing the logging call. |
| %(levelname)s | Text logging level for the message ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL') |
| %(lineno)d | Source line number where the logging call was issued (if available). |
| %(message)s | The logged message, computed as msg % args. This is set when Formatter.format() is invoked.|
| %(msecs)d | Millisecond portion of the time when the LogRecord was created. |
| %(name)s | Name of the logger used to log the call. |
| %(pathname)s | Full pathname of the source file where the logging call was issued (if available). |
| %(process)d | Process ID (if available). |
| %(processName)s | Process name (if available). |
| %(thread)d | Thread ID (if available). |
| %(threadName)s | Thread name (if available). |

"""
    )


def check_params(**kwargs):
    # Checking if mailing is enabled
    if kwargs.get('enable_mailing'):

        # Checking if mail from/to address is provided.
        if kwargs.get('mailfrom_addr') in ('', None, ' '):
            raise ArgumentError('Invalid MailFrom address argument.')
        if kwargs.get('mailto_addr') in ('', None, ' '):
            raise ArgumentError('Invalid MailTo address argument.')
        if kwargs.get('verify_credentials'):
            if not isinstance(kwargs.get('mail_credentials'), tuple):
                raise ArgumentError('Invalid MailCredentials Format')
            smtplib.SMTP(kwargs.get('mail_host')).login(*kwargs.get('mail_credentials'))

    if isinstance(kwargs.get('log_level'), int):
        warnings.warn('In versions > 2020.02.x, you should specify log levels in string format, '
                      'like "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL".\n'
                      'Accepting log levels in traditional "logging.XXXX format will be removed in later builds'
                      'for easier user experience."',
                      category=DeprecationWarning)


def init_logging(log_name='logger', log_directory='logs', log_mode='a', max_bytes=100 * 1024 * 1024,
                 rotate_when='d', rotate_interval=1, backup_count=20, encoding=None, delay=0,
                 log_level='INFO', console_log=True, rotation_criteria='size',
                 log_format='[%(asctime)s] -- %(levelname)s - %(filename)s -- %(funcName)s - Line no - %(lineno)d '
                            '-- %(message)s\n', enable_mailing=False, mail_host=None, mailfrom_addr=None,
                 mailto_addr=None, mail_subject='Exception Report', mail_credentials=None, verify_credentials=False, mail_secure=None,
                 mail_timeout=2.0):
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
    :param log_level: Log level. (DEBUG|INFO|WARNING|ERROR|CRITICAL)
    :type log_level: str
    :param console_log: Flag for turning console logging on or off.
    :type console_log: Boolean
    :param rotation_criteria: Type of rotation. Options: 'size' | 'time'
    :type rotation_criteria: str
    :param log_format: Log formatter for setting log pattern
    :type log_format: str
    :param enable_mailing: Flag to enable mailing in case of critical errors
    :type enable_mailing: Boolean
    :param mail_host: Host name of the email server
    :type mail_host: str
    :param mailfrom_addr: From email id for sending email
    :type mailfrom_addr: str
    :param mailto_addr: To email id for sending email
    :type mailto_addr: str
    :param mail_subject: Subject of email
    :type mail_subject: str
    :param mail_credentials: login credentials for sending email (username, password)
    :type mail_credentials: tuple
    :param mail_secure: Tuple having keyfile and certificate file for encrypting email. If None, no TLS encryption.
    :type mail_secure: tuple or None
    :param mail_timeout: Max wait time to connect to smtp server.
    :type mail_timeout: float
    :return: Logger object
    :rtype: Logger

    """

    try:
        # Checking arguments
        check_params(**locals())

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

        if rotation_criteria.lower() in ('timeandsize', 'sizeandtime'):
            warnings.warn('Using both time and size based rotation is in '
                          'experimental mode. \nPlease do not use in PROD environment',
                          category=ExperimentalFeatureWarning)
            debug_file_handler = SizedTimedRotatingFileHandler(debug_log_file_name, when=rotate_when,
                                                               interval=rotate_interval, backupCount=backup_count,
                                                               encoding=encoding, delay=delay, maxBytes=max_bytes)
            info_file_handler = SizedTimedRotatingFileHandler(info_log_file_name, when=rotate_when,
                                                              interval=rotate_interval, backupCount=backup_count,
                                                              encoding=encoding, delay=delay, maxBytes=max_bytes)
            warning_file_handler = SizedTimedRotatingFileHandler(warning_log_file_name, when=rotate_when,
                                                                 interval=rotate_interval, backupCount=backup_count,
                                                                 encoding=encoding, delay=delay, maxBytes=max_bytes)
            error_file_handler = SizedTimedRotatingFileHandler(error_log_file_name, when=rotate_when,
                                                               interval=rotate_interval, backupCount=backup_count,
                                                               encoding=encoding, delay=delay, maxBytes=max_bytes)
        elif rotation_criteria.lower() == 'time':
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
        else:
            # Log handlers for size based file rotation
            debug_file_handler = RotatingFileHandler(debug_log_file_name, mode=log_mode, maxBytes=max_bytes,
                                                     backupCount=backup_count, encoding=encoding, delay=delay)
            info_file_handler = RotatingFileHandler(info_log_file_name, mode=log_mode, maxBytes=max_bytes,
                                                    backupCount=backup_count, encoding=encoding, delay=delay)
            warning_file_handler = RotatingFileHandler(warning_log_file_name, mode=log_mode, maxBytes=max_bytes,
                                                       backupCount=backup_count, encoding=encoding, delay=delay)
            error_file_handler = RotatingFileHandler(error_log_file_name, mode=log_mode, maxBytes=max_bytes,
                                                     backupCount=backup_count, encoding=encoding, delay=delay)

        # Log handler for sending smtp mail
        smtp_handler = SMTPHandler(mailhost=mail_host, fromaddr=mailfrom_addr, toaddrs=mailto_addr,
                                   subject=mail_subject, credentials=mail_credentials, secure=mail_secure,
                                   timeout=mail_timeout)
        # Setting smtp log handler properties
        smtp_handler.setFormatter(log_formatter)
        smtp_handler.setLevel(logging.CRITICAL)
        smtp_handler.addFilter(MyFilter(logging.CRITICAL))

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

            if enable_mailing:
                log.addHandler(smtp_handler)

            log.addHandler(debug_file_handler)
            log.addHandler(info_file_handler)
            log.addHandler(warning_file_handler)
            log.addHandler(error_file_handler)

        # Checking if log level in 'str' format or 'int' format
        if isinstance(log_level, int):
            log.setLevel(log_level)
        else:
            log.setLevel(getattr(logging, log_level.upper()))

        return log

    except Exception:
        exception_message = traceback.format_exc()
        raise Exception('Error occurred in setting up logging. Details: %s' % str(exception_message))
