"""app.custom_queue

Module that contains the custom queue class.
"""
from queue import Queue
from datetime import datetime


class CustomQueue(Queue):
    def __init__(self, maxsize: int, name: str, count: int = 0):
        super(CustomQueue, self).__init__()
        # count: how many times should you divide to find the weight of the arithmetic mean
        self.count = count
        self.name = name
        self.maxsize = maxsize
        self.time = datetime.now()
