import asyncio
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
ports = {
    "customer": 5554,
    "order": 5555,
    "ingredients": 5556,
    "cook": 5557,
    "prepare": 5553,
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

    pull_socket = context.socket(zmq.PULL)
    pull_socket.connect(f"tcp://localhost:{ports[trigger[worker_name]]}")

    push_socket = context.socket(zmq.PUSH)
    push_socket.bind(f"tcp://*:{ports[worker_name]}")

    while True:
        order = await pull_socket.recv_json()
        await work_func[worker_name](order)
        push_socket.send_json(order)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: worker_id.py step_id")
        sys.exit(0)
    asyncio.run(worker(int(sys.argv[1])))
