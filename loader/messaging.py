import boto3
from settings import AWS_TOPIC, AWS_REGION

class MessagingQueue(object):
    def __init__(self, *args, **kwargs):
        self.connected = False
        self.error = ''
        self.topic = ''
        self.client = None

    def connect(self):
        if self.connected:
            return True

        try:
            self.client = boto3.client('sns', region_name=AWS_REGION)
            self.topic = self._get_topic(AWS_TOPIC)
            self.connected = True
            self.error = ''
        except StopIteration:
            print("Cannot establish queue connection")
            return False

    def _get_topic(self, topic):
        response = self.client.list_topcis()
        topic_name = next(
            t['TopicArn'] for t in response['Topics']
            if topic in t['TopicArn']
        )
        return topic_name


class Bucket(object):
    def __init__(self, *args, **kwargs):
        self.client = boto3.client('s3')

    def upload_file(self, image):
        pass

    def download_file(self, image):
        pass