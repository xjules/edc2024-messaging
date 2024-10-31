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
    "process_order": 10,
    "get_ingredients": 20,
    "cook": 30,
    "pack_and_hand_over": 10,
}

trigger = {
    "process_order": "customer",
    "get_ingredients": "process_order",
    "cook": "get_ingredients",
    "pack_and_hand_over": "cook",
}

next_step = {
    "customer": "process_order",
    "process_order": "get_ingredients",
    "get_ingredients": "cook",
    "cook": "pack_and_hand_over",
    "pack_and_hand_over": "customer",
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


async def main():
    if len(sys.argv) != 2:
        print("Usage: worker_id.py id")
        return
    worker_name = id2step[int(sys.argv[1])]
    context = zmq.asyncio.Context()

    orders_socket_sub = context.socket(zmq.SUB)
    orders_socket_sub.connect("tcp://localhost:5556")
    orders_socket_sub.setsockopt_string(zmq.SUBSCRIBE, worker_name)

    updates_socket_pub = context.socket(zmq.PUB)
    updates_socket_pub.connect("tcp://localhost:5557")

    print(f"{worker_name=} ready...")

    tasks = []
    if worker_name == "process_order":
        # publishing internal orders
        orders_socket_pub = context.socket(zmq.PUB)
        orders_socket_pub.bind("tcp://*:5556")

        # updates from workers
        updates_socket_sub = context.socket(zmq.SUB)
        updates_socket_sub.setsockopt_string(zmq.SUBSCRIBE, "")
        updates_socket_sub.bind("tcp://*:5557")

        async def publish_updates():
            while True:
                msg = await updates_socket_sub.recv_string()
                print(msg)
                await orders_socket_pub.send_string(msg)

        tasks.append(asyncio.create_task(publish_updates()))

    tasks.append(
        asyncio.create_task(
            do_order_and_notify(orders_socket_sub, updates_socket_pub, worker_name)
        ),
    )
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
