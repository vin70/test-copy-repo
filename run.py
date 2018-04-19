import asyncio
from loader.models import Loader

if __name__ == "__main__":
    print("Starting client...")

    client = Loader()
    # client.process_images()
    imgs = client.get_local_imgs()
    for img in imgs:
        labels = client.get_labels(img)
        client.print_labels(labels)
        labels_list = client.filter_labels(labels)
        print(labels_list)

    # ioloop = asyncio.get_event_loop()
    # asyncio.ensure_future(client.take_image())
    # asyncio.ensure_future(client.send_to_server())
    # ioloop.run_forever()
    # ioloop.close()