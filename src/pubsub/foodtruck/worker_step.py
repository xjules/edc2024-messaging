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

trigger_step = {
    "process_order": "place_order",
    "get_ingredients": "process_order",
    "cook": "get_ingredients",
    "pack_and_hand_over": "cook",
}


async def do_order_and_notify(orders_socket, updates_socket, step_name):
    while True:
        order = await orders_socket.recv_json()
        print(f"Worker step update {order=}")
        if order["step"] == trigger_step[step_name]:
            print(f"{step_name=} working on order: {order['order_id']}")
            await asyncio.sleep(work_time[step_name])
            await updates_socket.send_json(
                {"step": step_name, "order_id": order["order_id"]}
            )
            print(f"done and {step_name=} sent notification!")


async def main():
    if len(sys.argv) != 2:
        print("Usage: worker_step.py step_id")
        return
    step_name = id2step[int(sys.argv[1])]
    context = zmq.asyncio.Context()

    orders_socket = context.socket(zmq.SUB)
    orders_socket.connect("tcp://localhost:5556")
    orders_socket.setsockopt_string(zmq.SUBSCRIBE, "")

    updates_socket = context.socket(zmq.PUB)
    updates_socket.connect("tcp://localhost:5557")

    print(f"{step_name=} ready...")
    await do_order_and_notify(orders_socket, updates_socket, step_name)


if __name__ == "__main__":
    asyncio.run(main())
