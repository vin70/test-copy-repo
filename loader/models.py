import cProfile
import cv2
import boto3
from datetime import datetime
import asyncio
from os import listdir
from os.path import join, isfile
from settings import (
    AWS_REGION,
    AWS_ACCESS_KEY,
    AWS_ACCESS_SECRET_KEY,
    IMG_DIR,
    BASE_DIR
)

class Loader(object):

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.client = boto3.client(
            'rekognition',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_ACCESS_SECRET_KEY,
            region_name = AWS_REGION
        )
        self.img = None
        self.pr = cProfile.Profile()

    async def take_image(self):
        _, self.img = self.cam.read()
        asyncio.ensure_future(self.take_image())

    async def send_to_server(self):
        if self.img is not None:
            img = cv2.imencode('.jpg', self.img)[1].tostring()
            response = self.client.detect_labels(Image={'Bytes': img})
            self.img = None
                
            print('\nDetected labels')    
            for label in response['Labels']:
                print (label['Name'] + ' : ' + str(label['Confidence']))

            print('Done...')
        await asyncio.sleep(1)
        asyncio.ensure_future(self.send_to_server())

    def process_images(self):
        imgs = [f for f in listdir(IMG_DIR) if isfile(join(IMG_DIR, f))]
        res = ""
        for img in imgs:
            start_time = datetime.now()
            with open(join(IMG_DIR, img), "rb") as image:
                f = image.read()
                byte = bytearray(f)
            response = self.client.detect_labels(Image={'Bytes': byte})
            res += '\nDetected labels for image %s\n' % img
            for label in response['Labels']:
                res += label['Name'] + ' : ' + str(label['Confidence']) + "\n"
            end_time = datetime.now()
            took_time = end_time - start_time
            res += "Done... Took: %sms\n" % took_time.microseconds
        print(res)
        with open(join(BASE_DIR, "process_imgs.%s.log" % datetime.now()), "w+") as log:
            log.write(res)
            