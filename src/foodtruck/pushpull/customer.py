import asyncio
import random
import time

import zmq
import zmq.asyncio


async def customer():
    context = zmq.asyncio.Context()
    push_socket = context.socket(zmq.PUSH)
    push_socket.bind("tcp://*:5554")

    pull_socket = context.socket(zmq.PULL)
    pull_socket.connect("tcp://localhost:5553")

    async def orders():
        while True:
            order = {"item": random.choice(["hotdog", "ice-cream"])}
            await push_socket.send_json(order)
            await asyncio.sleep(20)

    async def notifications():
        while True:
            order = await pull_socket.recv_json()
            print(f"Got {order=}")
            print(f"order took {time.time() - order['start_time']} seconds")

    await asyncio.gather(
        asyncio.create_task(orders()), asyncio.create_task(notifications())
    )


if __name__ == "__main__":
    asyncio.run(customer())
