import asyncio
import json
import sys
import time

import zmq.asyncio

id2step = {
    1: "order",
    2: "ingredients",
    3: "cook",
    4: "prepare",
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


async def worker(worker_id):
    worker_name = id2step[worker_id]
    context = zmq.asyncio.Context()
    dealer_socket = context.socket(zmq.DEALER)
    dealer_socket.setsockopt(zmq.IDENTITY, worker_name.encode())
    dealer_socket.connect("tcp://localhost:5556")

    while True:
        [_, msg] = await dealer_socket.recv_multipart()
        order = json.loads(msg)
        order = await work_func[worker_name](order)
        await dealer_socket.send_multipart([b"", json.dumps(order).encode()])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: worker_id.py step_id")
        sys.exit(0)
    asyncio.run(worker(int(sys.argv[1])))
