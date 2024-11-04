import asyncio

import zmq.asyncio

next_step = {
    "customer": "order",
    "order": "ingredients",
    "ingredients": "cook",
    "cook": "prepare",
    "prepare": "customer",
}


async def router():
    context = zmq.asyncio.Context()
    router_socket = context.socket(zmq.ROUTER)
    router_socket.bind("tcp://*:5556")
    while True:
        [sender_id, _, msg] = await router_socket.recv_multipart()
        sender_name = sender_id.decode()
        print(f"Routing from {sender_name} to {next_step[sender_name]}")
        await router_socket.send_multipart([next_step[sender_name].encode(), b"", msg])


if __name__ == "__main__":
    asyncio.run(router())
