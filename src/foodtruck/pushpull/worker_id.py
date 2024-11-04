import asyncio
import sys
import time

import zmq.asyncio

from foodtruck.utils import do_work, id2step, next_step, ports, trigger


async def worker(worker_id):
    worker_name = id2step[worker_id]
    context = zmq.asyncio.Context()

    pull_socket = context.socket(zmq.PULL)
    pull_socket.connect(f"tcp://localhost:{ports[trigger[worker_name]]}")

    push_socket = context.socket(zmq.PUSH)
    push_socket.bind(f"tcp://*:{ports[worker_name]}")

    while True:
        order = await pull_socket.recv_json()
        order = await do_work(worker_name, order)
        push_socket.send_json(order)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: worker_id.py step_id")
        sys.exit(0)
    asyncio.run(worker(int(sys.argv[1])))
