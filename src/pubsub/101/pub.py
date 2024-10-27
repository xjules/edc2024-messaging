import asyncio
import time

import zmq
import zmq.asyncio


async def publisher():
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    while True:
        message = f"Update {int(time.time())}"
        await socket.send_string(message)
        print(f"Published: {message}")
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(publisher())
