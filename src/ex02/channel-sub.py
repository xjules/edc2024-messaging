import asyncio
import sys

import zmq
import zmq.asyncio


async def subscriber(channels):
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")

    for channel in channels:
        socket.setsockopt_string(zmq.SUBSCRIBE, channel)

    while True:
        message = await socket.recv_string()
        print(f"Received: {message}")


async def main():
    if len(sys.argv) < 2:
        print("Usage: script.py <channel1> [<channel2> ...]")
        return

    channels = sys.argv[1:]
    await subscriber(channels)


asyncio.run(main())
