import asyncio
from loader.models import Loader
from utils.thread import TaskThread


class Client(object):
    def __init__(self):
        super().__init__()
        self.loader = Loader()
        self.ioloop = asyncio.get_event_loop()
        task = self.ioloop.create_task(self.loader.task())
        self.ioloop.run_forever(task)
        
