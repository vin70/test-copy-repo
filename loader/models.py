import cProfile
import cv2
import boto3
import asyncio

class Loader(object):

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.client = boto3.client('rekognition','eu-west-1')
        self.img = None
        self.pr = cProfile.Profile()

    async def take_image(self):
        _, self.img = self.cam.read()
        asyncio.ensure_future(self.take_image())

    async def send_to_server(self):
        if self.img is not None:
            self.pr.enable()
            img = cv2.imencode('.jpg', self.img)[1].tostring()
            response = self.client.detect_labels(Image={'Bytes': img})
            self.img = None
                
            print('\nDetected labels')    
            for label in response['Labels']:
                print (label['Name'] + ' : ' + str(label['Confidence']))

            print('Done...')
            self.pr.disable()
            # self.pr.print_stats(sort='time')
        await asyncio.sleep(1)
        asyncio.ensure_future(self.send_to_server())
    