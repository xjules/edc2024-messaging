import asyncio
import json
import random
import time

import zmq
import zmq.asyncio


async def customer():
    context = zmq.asyncio.Context()
    dealer_socket = context.socket(zmq.DEALER)
    dealer_socket.setsockopt(zmq.IDENTITY, b"customer")
    dealer_socket.connect("tcp://localhost:5556")

    async def orders():
        while True:
            order = {"item": random.choice(["hotdog", "ice-cream"])}
            await dealer_socket.send_multipart([b"", json.dumps(order).encode()])
            await asyncio.sleep(20)

    async def notifications():
        while True:
            [_, msg] = await dealer_socket.recv_multipart()
            order = json.loads(msg)
            print(f"Got {order=}")
            print(f"order took {time.time() - order['start_time']} seconds")

    await asyncio.gather(
        asyncio.create_task(orders()), asyncio.create_task(notifications())
    )


if __name__ == "__main__":
    asyncio.run(customer())
