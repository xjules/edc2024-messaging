import asyncio
import random
import time

import zmq
import zmq.asyncio


async def publisher():
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    channels = ["sports", "weather", "news"]

    while True:
        channel = random.choice(channels)
        message = f"{channel} update at {time.time()}"
        await socket.send_string(f"{channel} {message}")
        print(f"Published: {message}")
        await asyncio.sleep(1)


asyncio.run(publisher())
