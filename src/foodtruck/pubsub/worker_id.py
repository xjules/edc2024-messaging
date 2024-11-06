import asyncio
import json
import sys

import zmq.asyncio

from foodtruck.utils import do_work, id2step, next_step


async def worker(stage_name):
    context = zmq.asyncio.Context()

    unit_socket = context.socket(zmq.SUB)
    unit_socket.connect("tcp://localhost:5556")
    unit_socket.setsockopt_string(zmq.SUBSCRIBE, stage_name)
    # stage_name in ("cust", "order", "ing", "cook", "prep")

    chef_socket = context.socket(zmq.PUB)
    chef_socket.connect("tcp://localhost:5557")
    print(f"{stage_name=} ready!")
    while True:
        msg = await unit_socket.recv_string()
        _, json_data = msg.split(" ", 1)
        order = json.loads(json_data)
        order = await do_work(stage_name, order)
        await chef_socket.send_string(next_step[stage_name] + " " + json.dumps(order))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: worker_id.py step_id")
        sys.exit(0)
    stage_name = id2step[int(sys.argv[1])]
    asyncio.run(worker(stage_name))
