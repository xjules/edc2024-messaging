import asyncio
import json
import sys

import zmq.asyncio

from foodtruck.utils import do_work, id2step, next_step


async def worker(worker_id):
    worker_name = id2step[worker_id]
    context = zmq.asyncio.Context()

    workers_socket = context.socket(zmq.SUB)
    workers_socket.connect("tcp://localhost:5556")
    workers_socket.setsockopt_string(zmq.SUBSCRIBE, worker_name)

    chef_socket = context.socket(zmq.PUB)
    chef_socket.connect("tcp://localhost:5557")
    print(f"{worker_name=} ready!")
    while True:
        msg = await workers_socket.recv_string()
        _, json_data = msg.split(" ", 1)
        order = json.loads(json_data)
        order = await do_work(worker_name, order)
        await chef_socket.send_string(next_step[worker_name] + " " + json.dumps(order))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: worker_id.py step_id")
        sys.exit(0)
    asyncio.run(worker(int(sys.argv[1])))
