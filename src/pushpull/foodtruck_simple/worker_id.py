import asyncio
import sys

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
ports = {
    "customer": 5554,
    "process_order": 5555,
    "get_ingredients": 5556,
    "cook": 5557,
    "pack_and_hand_over": 5558,
}


async def do_step_and_notify(pull_socket, push_socket, worker_name):
    order_id = 0
    while True:
        order = await pull_socket.recv_json()
        if worker_name == "process_order":
            order["order_id"] = order_id
            order_id += 1
            print(f"Received {order=}")
        elif worker_name == "pack_and_hand_over":
            order["status"] = "complete"
        print(f"{worker_name=} working the {order=}")
        await asyncio.sleep(work_time[worker_name])
        push_socket.send_json(order)


async def main():
    if len(sys.argv) != 2:
        print("Usage: worker_id.py step_id")
        sys.exit(0)

    worker_name = id2step[int(sys.argv[1])]
    context = zmq.asyncio.Context()

    pull_socket = context.socket(zmq.PULL)
    pull_socket.connect(f"tcp://localhost:{ports[trigger[worker_name]]}")

    push_socket = context.socket(zmq.PUSH)
    push_socket.bind(f"tcp://*:{ports[worker_name]}")

    print(f"{worker_name=} ready...")
    await do_step_and_notify(pull_socket, push_socket, worker_name)


if __name__ == "__main__":
    asyncio.run(main())
