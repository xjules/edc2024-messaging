import asyncio
import sys
import time

import zmq
import zmq.asyncio


async def subscriber():
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    while True:
        message = await socket.recv_string()
        print(f"Received: {message}")


if __name__ == "__main__":
    asyncio.run(subscriber())
