import asyncio
import json
import sys
import time

import zmq.asyncio

id2step = {
    1: "process_order",
    2: "get_ingredients",
    3: "cook",
    4: "pack_and_hand_over",
}

work_time = {
    "order": 10,
    "ingredients": 20,
    "cook": 30,
    "prepare": 10,
}

trigger = {
    "order": "customer",
    "ingredients": "order",
    "cook": "ingredients",
    "prepare": "cook",
}

next_step = {
    "customer": "order",
    "order": "ingredients",
    "ingredients": "cook",
    "cook": "prepare",
    "prepare": "customer",
}

order_id = 0


async def do_order(order):
    global order_id
    print("1. Processing the order...")
    order["order_id"] = order_id
    order["order"] = "ok"
    order_id += 1
    await asyncio.sleep(10)
    return order


async def ingredients(order):
    print("2. Getting ingredients...")
    time.sleep(2)
    order["ing"] = "ok"
    await asyncio.sleep(20)
    return order


async def cook(order):
    print("3. Cooking")
    order["cook"] = "ok"
    await asyncio.sleep(30)
    return order


async def prepare(order):
    print("4. Packing and handing over")
    order["prepare"] = "ok"
    await asyncio.sleep(10)
    return order


work_func = {
    "order": do_order,
    "ingredients": ingredients,
    "cook": cook,
    "prepare": prepare,
}


async def do_order_and_notify(orders_socket_sub, updates_socket_pub, worker_name):
    order_id = 0
    while True:
        msg = await orders_socket_sub.recv_string()
        _, json_data = msg.split(" ", 1)
        order = json.loads(json_data)
        print(f"Worker's update {order=}")
        if worker_name == "process_order":
            order["order_id"] = order_id
            order_id += 1
            order["start_time"] = time.time()
        elif worker_name == "pack_and_hand_over":
            order["status"] = "complete"

        print(f"{worker_name=} working the {order=}")

        await asyncio.sleep(work_time[worker_name])

        await updates_socket_pub.send_string(
            next_step[worker_name] + " " + json.dumps(order)
        )


async def worker(worker_id):
    worker_name = id2step[worker_id]
    context = zmq.asyncio.Context()

    workers_socket_sub = context.socket(zmq.SUB)
    workers_socket_sub.connect("tcp://localhost:5556")
    workers_socket_sub.setsockopt_string(zmq.SUBSCRIBE, worker_name)

    chef_socket_pub = context.socket(zmq.PUB)
    chef_socket_pub.connect("tcp://localhost:5557")

    while True:
        msg = await workers_socket_sub.recv_string()
        _, json_data = msg.split(" ", 1)
        order = json.loads(json_data)
        order = await work_func[worker_name](order)

        await chef_socket_pub.send_string(
            next_step[worker_name] + " " + json.dumps(order)
        )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: worker_id.py step_id")
        sys.exit(0)
    asyncio.run(worker(int(sys.argv[1])))
