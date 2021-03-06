import threading
import time
from app.custom_queue import CustomQueue
from app.logger import get_logger
from app.queues import Queues
from app.skier import SkierThread
from app.utils import random_bool

LOGGER = get_logger(__name__)


class ElevatorThread(threading.Thread):
    def __init__(self, queues: Queues, remaining_skiers: int, name=None):
        super(ElevatorThread, self).__init__()
        self.queues = queues
        self.remaining_skiers = remaining_skiers
        self.name = name

        # Used on report
        self.total_used_spaces = 0
        self.elevator_running_times = 1

        self.total_spaces = 4

        self.empy_spaces = self.total_spaces
        self.waiting_time = ''
        self.elevator_ref = ''

    def get_from(self, queue: CustomQueue, many: int = 1):
        for _ in range(many):
            skier: SkierThread = queue.get()
            self.empy_spaces -= 1

            skier_time = skier.queue_time()
            self.queues.add_time(queue, skier_time)
            self.waiting_time += f'Esquiador in {queue.name}: {skier_time} | '
            self.elevator_ref += f'{queue.name} '

    def run(self):
        while (self.remaining_skiers >= (self.total_spaces - 1)):
            # auxiliary variables
            self.empy_spaces = self.total_spaces
            self.elevator_ref = ""
            self.waiting_time = ""
            leftTriple = False
            rightTriple = False

            LS_size, LT_size, RT_size, RS_size = self.queues.queue_sizes()

            randomize_choice_for_triples = random_bool()

            if (randomize_choice_for_triples):
                if (LT_size > 2
                        and self.empy_spaces > 2):
                    self.get_from(self.queues.LT, 3)
                    leftTriple = True
            else:
                if (RT_size > 2
                        and self.empy_spaces > 2):
                    self.get_from(self.queues.RT, 3)
                    rightTriple = True

            if (not leftTriple and not rightTriple and (LS_size + RS_size) >= 3):

                randomize_choice_for_singles = random_bool()

                while (self.empy_spaces > 0
                        and (self.queues.LS.qsize() > 0
                             or self.queues.RS.qsize() > 0)):

                    if (randomize_choice_for_singles):
                        if (self.queues.LS.qsize() > 0):
                            self.get_from(self.queues.LS)

                        randomize_choice_for_singles = False
                    else:
                        if (self.queues.RS.qsize() > 0):
                            self.get_from(self.queues.RS)

                        randomize_choice_for_singles = True
            else:
                if (leftTriple
                        and RS_size > 0):
                    self.get_from(self.queues.RS)

                if (rightTriple
                        and LS_size > 0):
                    self.get_from(self.queues.LS)

            if self.remaining_skiers <= 7:
                # 7 pois seria a situa????o de melhor aproveitamento, onde ambas triplas, RT e LT, tem 2 (somando 4) e as singles, RS e LS, tem 1 e 2 (podendo ser 2 e 1).
                # Nessa situa????o, onde ?? sabido que n??o entrar?? mais ningu??m, o elevador ir?? consumir os 3 das singles e sobrar?? somente os 4 das triplas.
                # Como o consumo do elevator se baseia no estado das filas no in??cio do processo, nesse ponto, temos que considerar como 7.
                # Isto est?? no final do processo com objetivo de permitir que o consumo aconte??a antes de qualquer movimenta????o.
                self.move_leftover_skyers(RT_size, LT_size)

            self.sum_elevator_info()
            time.sleep(5)

        else:
            self.report()

    def move_leftover_skyers(self, RT_size: int, LT_size: int):
        LOGGER.debug('Tentar?? mover esquiadores entre filas')
        for _ in range(RT_size):
            self.queues.RS.put(self.queues.RT.get())
        for _ in range(LT_size):
            self.queues.LS.put(self.queues.LT.get())

    def sum_elevator_info(self):
        self.elevator_running_times += 1
        self.remaining_skiers -= (self.total_spaces - self.empy_spaces)
        self.total_used_spaces += self.total_spaces - self.empy_spaces
        LOGGER.debug(
            f"""print_info()
            {'###'*3}
            >Elevador {self.elevator_running_times}<
            Esquiadores que sairam: "{self.elevator_ref}"
            Tempos em fila dos esquiadores: "{self.waiting_time}"
            Falta sair: {self.remaining_skiers}
            {'###'*3}
            """)
        self.queues.count_queues_lenght()

    def report(self):
        utilization = self.total_used_spaces / \
            (self.total_spaces * self.elevator_running_times)
        LOGGER.info(f'aproveitamento = {utilization}')
        self.queues.report_queue_time()
