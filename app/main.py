"""app.main

Module that contains the main application.
"""
import time
from app.logger import get_logger

from datetime import datetime
from app.elevator import ElevatorThread
from app.skier import SkierThread
from app.queues import Queues

LOGGER = get_logger(__name__)


def app():
    """app.main

    Main application.
    """
    LOGGER.info('starting app')
    start_time = datetime.now()
    queues = Queues()
    max_skiers = 120

    c = ElevatorThread(queues, max_skiers, name='elevator')
    c.start()

    # TODO: tornar a criação uma thread por si ao invés de seguir com um while
    while(max_skiers):
        p = SkierThread(queues, name='organizer', daemon=True)
        p.start()
        max_skiers -= 1
        LOGGER.debug(f'falta entrar = {max_skiers}')
        time.sleep(1)

    c.join()
    LOGGER.info('everything ended well')
    LOGGER.info(f'finished in {datetime.now() - start_time}')
