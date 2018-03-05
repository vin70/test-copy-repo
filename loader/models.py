import cv2
import boto3
import asyncio

class Loader(object):

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.client = boto3.client('rekognition','eu-west-1')
        self.img = None

    async def task(self):
        _, self.img = self.cam.read()
        asyncio.ensure_future(self.task())

    async def send_to_server(self):
        if self.img is not None:
            img = cv2.imencode('.jpg', self.img)[1].tostring()
            response = self.client.detect_labels(Image={'Bytes': img})
                
            print('\nDetected labels')    
            for label in response['Labels']:
                print (label['Name'] + ' : ' + str(label['Confidence']))

            print('Done...')
        await asyncio.sleep(1)
        asyncio.ensure_future(self.send_to_server())
    