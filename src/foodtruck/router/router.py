import asyncio

import zmq.asyncio

from foodtruck.utils import next_step


async def router():
    context = zmq.asyncio.Context()
    router_socket = context.socket(zmq.ROUTER)
    router_socket.bind("tcp://*:5556")
    while True:
        [sender_id, _, msg] = await router_socket.recv_multipart()
        sender_name = sender_id.decode()
        receiver_name = next_step[sender_name]
        print(f"Routing from {sender_name} to {receiver_name}")
        await router_socket.send_multipart([receiver_name.encode(), b"", msg])


if __name__ == "__main__":
    asyncio.run(router())
