import threading
from datetime import datetime
from app.logger import get_logger
from app.custom_queue import CustomQueue

LOGGER = get_logger(__name__)


class SkierThread(threading.Thread):
    def __init__(self, queues: CustomQueue, name=None, daemon=None):
        super(SkierThread, self).__init__()
        self.queues = queues
        self.name = name
        self.daemon = daemon
        self.start_time = datetime.now()

    def queue_time(self):
        departure_time = datetime.now()
        return departure_time - self.start_time

    def run(self):
        LS_size, LT_size, RT_size, RS_size = self.queues.queue_sizes()

        if (LS_size < RS_size
            and LS_size < (LT_size * 2)
                and LS_size < (RT_size * 2)):
            self.queues.add_to_LS(self)

        elif (RS_size <= LS_size
              and RS_size < (RT_size * 2)
              and RS_size < (LT_size * 2)):
            self.queues.add_to_RS(self)

        elif (LT_size <= RT_size):
            self.queues.add_to_LT(self)

        else:
            self.queues.add_to_RT(self)

        self.queues.count_queues_lenght()
