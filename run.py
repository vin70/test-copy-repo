import asyncio
import cProfile
from loader.models import Loader

if __name__ == "__main__":
    print("Starting client...")

    client = Loader()

    ioloop = asyncio.get_event_loop()
    asyncio.ensure_future(client.take_image())
    asyncio.ensure_future(client.send_to_server())
    ioloop.run_forever()
    ioloop.close()