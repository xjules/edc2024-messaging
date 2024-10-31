import asyncio
import json
import random
import time

import zmq
import zmq.asyncio


async def customer():
    context = zmq.asyncio.Context()
    orders_socket_sub = context.socket(zmq.SUB)
    orders_socket_sub.connect("tcp://localhost:5556")
    orders_socket_sub.setsockopt_string(zmq.SUBSCRIBE, "customer")

    updates_socket_pub = context.socket(zmq.PUB)
    updates_socket_pub.connect("tcp://localhost:5557")

    products = ["hotdog", "hamburger", "ice-cream"]

    async def orders():
        while True:
            # Create order
            order = {"item": random.choice(products)}

            print(f"Customer with {order=}")

            # Send order and wait for response
            await updates_socket_pub.send_string("process_order " + json.dumps(order))
            await asyncio.sleep(20)

    async def notifications():
        while True:
            msg = await orders_socket_sub.recv_string()
            _, json_data = msg.split(" ", 1)
            order = json.loads(json_data)
            print(f"Got {order=}")
            print(f"order took {time.time() - order['start_time']} seconds")

    await asyncio.gather(
        asyncio.create_task(orders()), asyncio.create_task(notifications())
    )


if __name__ == "__main__":
    asyncio.run(customer())
