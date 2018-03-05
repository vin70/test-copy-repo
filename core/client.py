import cv2
from loader.models import Loader
from utils.thread import TaskThread


class Client(object):
    def __init__(self):
        super().__init__()
        self.loader = Loader()
        
