from app.custom_queue import CustomQueue
from app.logger import get_logger
from datetime import datetime, timedelta

LOGGER = get_logger(__name__)
QUEUE_MAX_SIZE = 20


class Queues():
    def __init__(self):
        self.LS = CustomQueue(QUEUE_MAX_SIZE, 'LeftSingle')
        self.LT = CustomQueue(QUEUE_MAX_SIZE, 'LeftTriple')
        self.RT = CustomQueue(QUEUE_MAX_SIZE, 'RightTriple')
        self.RS = CustomQueue(QUEUE_MAX_SIZE, 'RightSingle')

        self.starting_time = datetime.now()

        self.Total_time = self.starting_time

    def add_time(self, queue: CustomQueue, time: timedelta):
        self.Total_time += time
        queue.time += time
        queue.count += 1

    def add_to_LS(self, skyer):
        self.add_to(self.LS, skyer)

    def add_to_LT(self, skyer):
        self.add_to(self.LT, skyer)

    def add_to_RT(self, skyer):
        self.add_to(self.RT, skyer)

    def add_to_RS(self, skyer):
        self.add_to(self.RS, skyer)

    def add_to(self, queue: CustomQueue, skyer):
        queue.put(skyer)
        LOGGER.debug(f'Esquiador entrou na fila: {queue.name}')

    def normalize_time(self):
        self.Total_time -= self.starting_time
        self.LS.time -= self.starting_time
        self.LT.time -= self.starting_time
        self.RT.time -= self.starting_time
        self.RS.time -= self.starting_time

    def report_queue_time(self):
        self.normalize_time()

        total_count = self.LS.count + self.LT.count + self.RT.count + self.RS.count

        if total_count:
            LOGGER.info(f'Total time = {self.Total_time/total_count}')
        else:
            LOGGER.info('ninguem saiu de qualquer fila')

        if self.LS.count:
            LOGGER.info(f'{self.LS.name} time = {self.LS.time/self.LS.count}')
        else:
            LOGGER.info(f'ninguem saiu da fila {self.LS.name}')

        if self.LT.count:
            LOGGER.info(f'{self.LT.name} time = {self.LT.time/self.LT.count}')
        else:
            LOGGER.info(f'ninguem saiu da fila {self.LT.name}')

        if self.RT.count:
            LOGGER.info(f'{self.RT.name} time = {self.RT.time/self.RT.count}')
        else:
            LOGGER.info(f'ninguem saiu da fila {self.RT.name}')

        if self.RS.count:
            LOGGER.info(f'{self.RS.name} time = {self.RS.time/self.RS.count}')
        else:
            LOGGER.info(f'ninguem saiu da fila {self.RS.name}')

    def queue_sizes(self):
        LS_size = self.LS.qsize()
        LT_size = self.LT.qsize()
        RT_size = self.RT.qsize()
        RS_size = self.RS.qsize()
        return [LS_size, LT_size, RT_size, RS_size]

    def count_queues_lenght(self):
        LS_size, LT_size, RT_size, RS_size = self.queue_sizes()
        LOGGER.debug(
            f"""count_queues_lenght()
            {'###'*3}
            >Filas agora<
            LeftSingle: {LS_size}
            LeftTriple: {LT_size}
            RightTriple: {RT_size}
            RightSingle: {RS_size}
            {'###'*3}
            """)
