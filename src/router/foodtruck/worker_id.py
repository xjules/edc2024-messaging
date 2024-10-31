import asyncio
import json
import sys
import time

import zmq.asyncio

work_time = {
    "process_order": 10,
    "get_ingredients": 20,
    "cook": 30,
    "pack_and_hand_over": 10,
}

id2step = {
    1: "process_order",
    2: "get_ingredients",
    3: "cook",
    4: "pack_and_hand_over",
}

next_step = {
    "customer": "process_order",
    "process_order": "get_ingredients",
    "get_ingredients": "cook",
    "cook": "pack_and_hand_over",
    "pack_and_hand_over": "customer",
}


async def router(router_socket):
    order_id = 0
    while True:
        [sender_id, _, msg] = await router_socket.recv_multipart()
        order = json.loads(msg)
        sender_name = sender_id.decode()
        print(sender_name, order)
        if sender_name == "customer":
            order["order_id"] = order_id
            order_id += 1
            order["start_time"] = time.time()
        elif sender_name == "pack_and_hand_over":
            order["status"] = "complete"

        print(f"Order {order}: routing from {sender_name} to {next_step[sender_name]}")
        await router_socket.send_multipart(
            [next_step[sender_name].encode(), b"", json.dumps(order).encode()]
        )


async def do_order_and_notify(worker_name, dealer_socket):
    while True:
        print(f"{worker_name} ready to action!")
        [_, msg] = await dealer_socket.recv_multipart()
        order = json.loads(msg)

        print(f"{worker_name} processing {order=}")
        await asyncio.sleep(work_time[worker_name])
        await dealer_socket.send_multipart([b"", msg])
        # result = {
        #     "order_id": order["order_id"],
        #     "worker_id": worker_name,
        #     "status": "completed",
        # }
        # await dealer_socket.send_multipart([b"", json.dumps(result).encode()])


async def main():
    if len(sys.argv) != 2:
        print("Usage: worker_id.py step_id")
        sys.exit(0)
    worker_name = id2step[int(sys.argv[1])]
    context = zmq.asyncio.Context()
    dealer_socket = context.socket(zmq.DEALER)
    dealer_socket.setsockopt(zmq.IDENTITY, worker_name.encode())
    dealer_socket.connect("tcp://localhost:5556")

    print(f"Initiating worker {worker_name}")

    tasks = []
    if worker_name == "process_order":
        router_socket = context.socket(zmq.ROUTER)
        router_socket.bind("tcp://*:5556")

        tasks.append(asyncio.create_task(router(router_socket)))

    tasks.append(asyncio.create_task(do_order_and_notify(worker_name, dealer_socket)))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
