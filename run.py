import asyncio
import sys
from loader.models import Loader

if __name__ == "__main__":

    client = Loader()
    if 'camera' in sys.argv:
        print("Starting camera process...")
        ioloop = asyncio.get_event_loop()
        asyncio.ensure_future(client.take_image())
        asyncio.ensure_future(client.send_to_server())
        ioloop.run_forever()
        ioloop.close()
    else:
        print("Starting image process...")
        imgs = client.get_local_imgs()
        for img in imgs:
            labels = client.get_labels(img)
            client.print_labels(labels)
            filtered_lables = client.filter_labels(labels)
            print(filtered_lables)
