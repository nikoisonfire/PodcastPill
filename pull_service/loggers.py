from datetime import datetime
import logging.handlers
import logging
import sys

# Create the root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# Create the console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# Create the file handler
file_handler = logging.handlers.TimedRotatingFileHandler(
    filename='logs/{:%Y-%m-%d}.log'.format(datetime.now()),
    when='D',
    interval=1,
    backupCount=7
)
file_handler.setLevel(logging.WARNING)

# Create the formatter
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s', '%Y-%m-%d %H:%M:%S')

# Set the formatter for the handlers
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add the handlers to the root logger
root_logger.addHandler(console_handler)
root_logger.addHandler(file_handler)