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

objects_of_interest = {
    'Outdoors': {
        'threshold': 50.0,
        'byte': 1,
        'synonyms': [
            'Snow',
            'Landscape',
            'Scenery',
            'Sand',
            'Soil',
            'Nature',
            'Tree',
            'Flora',
            'Plant',
            'Birch',
            'Forest',
            'Grove',
            'Land',
            'Oak',
            'Sycamore',
            'City',
            'Urban',
        ]
    },
    'Path': {
        'threshold': 50.0,
        'byte': 2,
        'synonyms': [
            'Road',
            'Asphalt',
            'Sidewalk',
            'Walkway',
            'Walking',
            'Trail',
            'Alley',
            'Alleyway',
            'Road',
            'Pavement',
            'Street',
            'Park',
            'Freeway',
            'Highway',
            'Intersection'
        ]        
    },
    'Obstacle': {
        'threshold': 50.0,
        'byte': 3,
        'synonyms': [
            'Dirt Road',
            'Gravel',
            'Brick',
            'Parking',
            'Flagstone',
            'Column',
            'Pillar',
            'Fence',
            'Water',
            'Offroad'
        ]
    },
    'Sign': {
        'threshold': 50.0,
        'byte': 5,
        'synonyms': []
    },
    'Car': {
        'threshold': 50.0,
        'byte': 7,
        'synonyms': [
            'Automobile',
            'Transportation',
            'Vehicle',
            'Suv',
            'Sedan',
        ]        
    },
    'Human': {
        'threshold': 50.0,
        'byte': 8,
        'synonyms': []
    }
}

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

    def get_labels(self, img):
        print ('\nLoading image %s\n' % img)
        with open(join(IMG_DIR, img), "rb") as image:
            f = image.read()
            byte = bytearray(f)
        response = self.client.detect_labels(Image={'Bytes': byte})

        return response['Labels']

    def print_labels(self, labels):
        print('\nDetected labels')    
        for label in labels:
            print (label['Name'] + ' : ' + str(label['Confidence']))

    def process_images(self):
        imgs = [f for f in listdir(IMG_DIR) if isfile(join(IMG_DIR, f))]
        res = ""
        for img in imgs:
            start_time = datetime.now()
            labels = self.get_labels(img)
            res += 'Detected labels for image %s\n' % img
            self.print_labels(labels)
            for label in labels:
                res += label['Name'] + ' : ' + str(label['Confidence']) + "\n"
            end_time = datetime.now()
            took_time = end_time - start_time
            res += "Done... Took: %sms\n" % took_time.microseconds
        print(res)
        with open(join(BASE_DIR, "process_imgs.%s.log" % datetime.now()), "w+") as log:
            log.write(res)

    def get_bytes_from_labels(self, labels):
        bytes_res = []
        for label in labels:
            if label['Name'] in objects_of_interest.keys():
                if label['Confidence'] >= objects_of_interest[label['Name']]['threshold']:
                    bytes_res.append(objects_of_interest[label['Name']]['byte'].to_bytes(8, byteorder='big', signed=True))

        return bytes_res

    def filter_labels(self, labels):
        res = []
        for label in labels:
            if label['Name'] in objects_of_interest.keys():
                if label['Name'] not in res:
                    res.append(label['Name'])
            else:
                for key, val in objects_of_interest.items():
                    if label['Name'] in val['synonyms']:
                        if key not in res:
                            res.append(key)

        return res


    def get_local_imgs(self):
        return [f for f in listdir(IMG_DIR) if isfile(join(IMG_DIR, f))]