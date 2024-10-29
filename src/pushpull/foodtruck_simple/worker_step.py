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
    "get_ingredients": "process_order",
    "cook": "get_ingredients",
    "pack_and_hand_over": "cook",
}
ports_step = {
    "process_order": 5555,
    "get_ingredients": 5556,
    "cook": 5557,
    "pack_and_hand_over": 5558,
}


async def do_step_and_notify(receiver, sender, step_name):
    while True:
        order = await receiver.recv_json()
        print(f"Worker step update {order=}")
        if order["step"] == trigger_step[step_name]:
            print(f"{step_name=} working on order: {order['order_id']}")
            await asyncio.sleep(work_time[step_name])
            await sender.send_json({"step": step_name, "order_id": order["order_id"]})
            print(f"done and {step_name=} sent notification!")


async def monitor_order(customer_socket, sender):
    while True:
        # Wait for order
        order = await customer_socket.recv_json()
        print(f"Received order: {order}")
        await asyncio.sleep(work_time["process_order"])
        await sender.send_json({"step": "process_order", "order_id": order["order_id"]})


async def main():
    if len(sys.argv) != 2:
        print("Usage: worker_step.py step_id")
        return
    step_name = id2step[int(sys.argv[1])]
    context = zmq.asyncio.Context()
    # Connect to receive work from previous step
    customer_socket = context.socket(zmq.REP)
    customer_socket.bind("tcp://*:5555")
    receiver = context.socket(zmq.PULL)
    input_port = ports_step[step_name]
    receiver.connect(f"tcp://localhost:{input_port}")

    # Bind to send work to next step
    sender = context.socket(zmq.PUSH)
    output_port = input_port + 1
    sender.bind(f"tcp://*:{output_port}")

    print(f"{step_name=} ready...")
    consumer_task = None
    if step_name == "process_order":
        # consumer_task = asyncio.create_task(monitor_order())
        await monitor_order(customer_socket, sender)
    else:
        await do_step_and_notify(receiver, sender, step_name)
    if consumer_task:
        await consumer_task


if __name__ == "__main__":
    asyncio.run(main())
