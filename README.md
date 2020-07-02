# autopylogger

Python thread-safe logging wrapper module with out of box log rotation and critical logs mailing facility built for seamless integration in any python script.

Requirements: logging

#### Basic Usage :

- Initialize your logger object by calling the 'init_logging' function *(with mailing feature turned OFF)*

        from autopylogger import init_logging
        my_logger_obj = init_logging(log_name='my_logs', log_directory='logs_dir')

- Initialize your logger object by calling the 'init_logging' function *(with mailing feature turned ON)*

        from autopylogger import init_logging
        my_logger_obj = init_logging(log_name='my_logs', log_directory='logs_dir', enable_mailing=True, mail_host='mymail.host.com', mailfrom_addr='<email_address>', mailto_addr='<email_address>', mail_subject='<subject>', mail_credentials=('<username>', '<password>'))


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
    
    *NOTE: It is adviced to turn OFF console logging in production environments when your program is running as service to  prevent flushing of system console logs with your info messages. Eg: In linux systems.*
    
- **Setting log rotation criteria:** *Pass the appropriate value to the **"rotation_criteria"** flag.*

        rotation_criteria = 'size' | 'time' | 'timeandsize'

  By default, rotation criteria **"size"** is used with max file size of 200 Mbs.
  
  - When choosing 'size' based rotation criteria, pass the argument value **'max_bytes'** to specify the max size of log file in bytes.

        'rotation_criteria' = 'size'
        'max_bytes' = 5*1024*1024

  - When choosing **"time"** based rotation criteria, pass the argument value **"rotate_when"** & **"rotate_interval"**.

        'rotation_criteria' = 'time'
        'rotate_when' = 'd' | 'h' | 'm' | 's'
        'rotate_interval' = 1 (for rotating log every 1 day|hour|minute|second)
  
  - When choosing **"timeandsize"** based rotation criteria, pass the argument value **"rotate_when"**,**"rotate_interval"** & **'max_bytes'**.
        
        'mail_host' = 'mail server hostname or ip address'
        'rotation_criteria' = 'timeandsize'
        'max_bytes' = 5*1024*1024
        'rotate_when' = 'd' | 'h' | 'm' | 's'
        'rotate_interval' = 1 (for rotating log every 1 day|hour|minute|second)
        
  *NOTE: In "timeandsize" rotation criteria, a file is rotate when either of the time or size constraint gets satisfied."*
  
  
- **Turning critical mailing ON/OFF:** *Pass the boolean value (TRUE|FALSE) to the **"enable_mailing"** flag. By default mailing is enabled for critical errors.*
   
  - When **"enable_mailing"** is set to True, following flags are required. 

        'mailfrom_addr' = '<Sender email address>'
        'mailto_addr' = '<Receiver email address>'
        'mail_subject' = '<Mail subject>'
        'mail_credentials' = ('<username>', '<password>') or None if no authentication is required.
  

- **Setting log format:** *Pass the desired log format string to the **"log_format"** flag*

        log_format='[%(asctime)s] -- %(levelname)s - %(filename)s -- %(funcName)s - Line no - %(lineno)d -- %(message)s'

##### Log formatter arguments:
   
| Format | Description |
| ------ | ------ |
| %(asctime)s | Human-readable time when the LogRecord was created. By default this is of the form ‘2003-07-08 16:49:45,896’ (the numbers after the comma are millisecond portion of the time). |
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

