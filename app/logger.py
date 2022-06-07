"""app.logging

Module that contains the default application logger configuration.
"""

import logging
import os

test_log = os.getenv('TEST_LOG', 'False').lower() in ('true', '1', 't')
log_level = os.getenv('LOG_LEVEL', 'INFO')
FORMAT_LOG = '%(asctime)s : %(name)s : %(levelname)s - %(message)s'
TEST_MSG = 'This message should go to the log file and the stream output, like Øresund and Malmö'

def get_logger(name):
    """get_logger

    Args:
        name (str): name of the logger

    Returns:
        Logger: a usable logger
    """
    stream_handler =  logging.StreamHandler()
    file_handler = logging.FileHandler('example.log', encoding='utf-8')

    logging.basicConfig(
        level=log_level,
        format=FORMAT_LOG,
        handlers=[file_handler, stream_handler]
        )
    logger = logging.getLogger(name)

    if test_log:
        logger.critical('starting test logger')
        logger.debug(TEST_MSG)
        logger.info(TEST_MSG)
        logger.warning(TEST_MSG)
        logger.error(TEST_MSG)
        logger.critical('ending test logger')

    return logger
