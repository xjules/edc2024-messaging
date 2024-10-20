import asyncio
import sys
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


async def subscriber():
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    while True:
        message = await socket.recv_string()
        print(f"Received: {message}")


async def main():
    if len(sys.argv) != 2:
        print("Usage: script.py [0/1]")
        print("0 - Run as publisher")
        print("1 - Run as subscriber")
        return

    if sys.argv[1] == "0":
        print("Running as publisher...")
        await publisher()
    elif sys.argv[1] == "1":
        print("Running as subscriber...")
        await subscriber()
    else:
        print("Invalid argument. Use 0 for publisher or 1 for subscriber.")


if __name__ == "__main__":
    asyncio.run(main())
