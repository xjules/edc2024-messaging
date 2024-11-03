import asyncio

import zmq.asyncio


async def update(msg):
    return msg


async def chef():
    context = zmq.asyncio.Context()

    print("Chef ready...")
    workers_socket_pub = context.socket(zmq.PUB)
    workers_socket_pub.bind("tcp://*:5556")

    chef_socket_sub = context.socket(zmq.SUB)
    chef_socket_sub.setsockopt_string(zmq.SUBSCRIBE, "")
    chef_socket_sub.bind("tcp://*:5557")
    while True:
        msg = await chef_socket_sub.recv_string()
        msg = await update(msg)
        await workers_socket_pub.send_string(msg)


if __name__ == "__main__":
    asyncio.run(chef())
