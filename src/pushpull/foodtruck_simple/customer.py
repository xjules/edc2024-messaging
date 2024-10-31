import asyncio
import random

import zmq
import zmq.asyncio


async def customer():
    context = zmq.asyncio.Context()
    push_socket = context.socket(zmq.PUSH)
    push_socket.bind("tcp://*:5554")

    pull_socket = context.socket(zmq.PULL)
    pull_socket.bind("tcp://*:5553")

    products = ["hotdog", "hamburger", "ice-cream"]

    async def orders():
        while True:
            # Create order
            order = {"item": random.choice(products)}

            print(f"Customer with {order=}")

            # Send order and wait for response
            await push_socket.send_json(order)
            await asyncio.sleep(20)

    async def notifications():
        while True:
            order = await pull_socket.recv_json()

            print(f"Got {order=}")

    await asyncio.gather([await orders(), await notifications()])


if __name__ == "__main__":
    asyncio.run(customer())
