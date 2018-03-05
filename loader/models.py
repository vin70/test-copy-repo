import cv2
from utils.thread import TaskThread

class Loader(TaskThread):

    def __init__(self):
        super().__init__()
        self._interval = 2
        self.cam = cv2.VideoCapture(0)
        self.run()

    def task(self):
        _, img = self.cam.read()
        # self.show_img(img)
        self.send_to_server(img)

    def show_img(self, image):
        if image is not None:
            cv2.imshow('Preview', image)

    def shutdown(self):
        cv2.destroyAllWindows()
        super().shutdown()

    def send_to_server(self, image):
        print("Sending image to server...")
        cv2.imwrite('temp.jpg', image)
    