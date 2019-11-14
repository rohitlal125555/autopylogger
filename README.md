
# python_log_rotate
Python thread-safe logging wrapper module with out of box log rotation facility built for seamless integration in any python script.

Requirements: logging

Usage :

Step 1: Initialize your logger object by calling the 'init_logging' function
	
	from python_log_rotate import init_logging
	my_logger_obj = init_logging(log_name'my_logs', log_directory='logs_dir')

Step 2: Use the object for writing DEBUG|INFO|WARNING|ERROR logs

	my_logger_obj.debug('This is DEBUG log')
	my_logger_obj.info('This is INFO log')
	my_logger_obj.warning('This is WARNING log')
	my_logger_obj.error('This is ERROR log')


Important Flags:

* Setting log level: Pass the appropriate value to the 'log_level' flag.
	log_level = logging.DEBUG | logging.INFO | logging.WARNING | logging.ERROR

* Turning console logging ON/OFF: Pass the appropriate vlaue to the 'console_log' flag.
	console_log = True | False

* Setting log rotation criteria: Pass the appropriate value to the 'rotation_criteria' flag.
	rotation_criteria = 'size' | 'time'

	By default, rotation criteria 'size' is used with max file size of 200 Mbs.
	
	--> When choosing 'size' based rotation critera, pass the argument value 'max_bytes' to specify the max size of log file in Kbs.
	--> When choosing 'time' based rotation critera, pass the argument value 'rotate_when' & 'rotate_interval'.

		'rotate_when' = 'd' | 'h' | 'm' | 's'
		'rotate_interval' = 1 (for rotating log every 1 day|hour|minute|second)
