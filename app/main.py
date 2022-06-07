"""app.main

Module that contains the main application.
"""
from app.logger import get_logger

LOGGER = get_logger(__name__)


def app():
    """app.main

    Main application.
    """
    LOGGER.info('starting app')
