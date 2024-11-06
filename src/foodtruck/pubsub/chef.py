import asyncio

import zmq.asyncio


def update(msg):
    print(f"message for chef {msg=}")
    return msg


async def chef():
    context = zmq.asyncio.Context()

    unit_socket = context.socket(zmq.PUB)
    unit_socket.bind("tcp://*:5556")

    chef_socket = context.socket(zmq.SUB)
    chef_socket.setsockopt_string(zmq.SUBSCRIBE, "")
    chef_socket.bind("tcp://*:5557")
    print("Chef ready!")
    while True:
        msg = await chef_socket.recv_string()
        msg = update(msg)
        await unit_socket.send_string(msg)


if __name__ == "__main__":
    asyncio.run(chef())
