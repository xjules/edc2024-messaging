import asyncio
import json
import sys

import zmq.asyncio

from foodtruck.utils import do_work, id2step, next_step


# stage_name in ("cust", "order", "ing", "cook", "prep")
async def stage(stage_name, context):
    all_socket = context.socket(zmq.SUB)
    all_socket.connect("tcp://localhost:5556")
    all_socket.setsockopt_string(zmq.SUBSCRIBE, stage_name)

    chef_socket = context.socket(zmq.PUB)
    chef_socket.connect("tcp://localhost:5557")
    print(f"{stage_name=} ready!")
    while True:  # stage job
        msg = await all_socket.recv_string()
        _, json_data = msg.split(" ", 1)
        order = json.loads(json_data)
        order = await do_work(stage_name, order)
        new_topic = next_step[stage_name]
        space = " "
        json_data = json.dumps(order)
        await chef_socket.send_string(new_topic + space + json_data)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: worker_id.py step_id")
        sys.exit(0)
    stage_name = id2step[int(sys.argv[1])]
    context = zmq.asyncio.Context()
    asyncio.run(stage(stage_name, context))
