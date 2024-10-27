import asyncio

import zmq.asyncio

from .ports import PORTS


async def send_orders(socket):
    order_id = 0
    while True:
        order = {"order_id": order_id, "item": "hotdog", "steps_completed": []}
        print(f"\n➡️ Placing order: {order_id}")
        await socket.send_json(order)
        order_id += 1
        await asyncio.sleep(3)


async def receive_completed_orders(socket):
    while True:
        order = await socket.recv_json()
        print(f"🎉 Completed order {order['order_id']}")
        print(f"Steps: {' -> '.join(order['steps_completed'])}")


async def main():
    context = zmq.asyncio.Context()

    # Connect to first step (food truck)
    sender = context.socket(zmq.PUSH)
    sender.connect(f"tcp://localhost:{PORTS['STEP_0']}")

    # Connect to receive completed orders
    receiver = context.socket(zmq.PULL)
    receiver.connect(f"tcp://localhost:{PORTS['COMPLETED']}")

    tasks = [
        asyncio.create_task(send_orders(sender)),
        asyncio.create_task(receive_completed_orders(receiver)),
    ]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
