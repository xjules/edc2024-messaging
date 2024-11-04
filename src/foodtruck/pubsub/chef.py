import asyncio

import zmq.asyncio


def update(msg):
    print(f"message for chef {msg=}")
    return msg


async def chef():
    context = zmq.asyncio.Context()

    workers_socket = context.socket(zmq.PUB)
    workers_socket.bind("tcp://*:5556")

    chef_socket = context.socket(zmq.SUB)
    chef_socket.setsockopt_string(zmq.SUBSCRIBE, "")
    chef_socket.bind("tcp://*:5557")
    print("Chef ready!")
    while True:
        msg = await chef_socket.recv_string()
        msg = update(msg)
        await workers_socket.send_string(msg)


if __name__ == "__main__":
    asyncio.run(chef())
