import asyncio
import json

import numpy as np
import zmq
import zmq.asyncio

context = zmq.asyncio.Context()


async def producer():
    """Produces chunks of numbers to sum"""
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://*:5557")

    _id = 0
    while True:
        numbers = np.random.randn((50))

        task = {"num_id": _id, "numbers": list(numbers)}
        print(f"Sending numbers with {_id=}")
        await socket.send_json(task)
        await asyncio.sleep(1)  # Pause between chunks
        _id += 1


if __name__ == "__main__":
    asyncio.run(producer())
