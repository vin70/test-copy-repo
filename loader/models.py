import cv2

class Loader(object):

    def __init__(self):
        self.run()

    def run(self):
        cam = cv2.VideoCapture(0)
        while True:
            ret_val, img = cam.read()
            cv2.imshow('Preview', img)
            if cv2.waitKey(1) == 27: 
                break  # esc to quit
        cv2.destroyAllWindows()


    