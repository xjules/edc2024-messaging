import asyncio
import json
import random
import time

import zmq
import zmq.asyncio


async def customer():
    context = zmq.asyncio.Context()
    workers_socket = context.socket(zmq.SUB)
    workers_socket.connect("tcp://localhost:5556")
    workers_socket.setsockopt_string(zmq.SUBSCRIBE, "customer")

    chef_socket = context.socket(zmq.PUB)
    chef_socket.connect("tcp://localhost:5557")

    async def orders():
        while True:
            order = {"item": random.choice(["hotdog", "hamburger", "ice-cream"])}
            await chef_socket.send_string("order " + json.dumps(order))
            await asyncio.sleep(20)

    async def notifications():
        while True:
            msg = await workers_socket.recv_string()
            _, json_data = msg.split(" ", 1)
            order = json.loads(json_data)
            print(f"Got {order=}")
            print(f"order took {time.time() - order['start_time']} seconds")

    await asyncio.gather(
        asyncio.create_task(orders()), asyncio.create_task(notifications())
    )


if __name__ == "__main__":
    asyncio.run(customer())
