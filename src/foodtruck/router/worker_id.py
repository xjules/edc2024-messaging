import asyncio
import json
import sys
import time

import zmq.asyncio

from foodtruck.utils import do_work, id2step


async def worker(worker_name):
    context = zmq.asyncio.Context()
    dealer_socket = context.socket(zmq.DEALER)
    dealer_socket.setsockopt(zmq.IDENTITY, worker_name.encode())
    dealer_socket.connect("tcp://localhost:5556")

    while True:
        [_, msg] = await dealer_socket.recv_multipart()
        order = json.loads(msg)
        order = await do_work(worker_name, order)
        await dealer_socket.send_multipart([b"", json.dumps(order).encode()])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: worker_id.py step_id")
        sys.exit(0)
    worker_name = id2step[int(sys.argv[1])]
    asyncio.run(worker(worker_name))
