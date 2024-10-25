import asyncio
import json
import sys

import numpy as np
import zmq
import zmq.asyncio

context = zmq.asyncio.Context()


async def worker(worker_id):
    pull_socket = context.socket(zmq.PULL)
    pull_socket.connect("tcp://localhost:5557")

    push_socket = context.socket(zmq.PUSH)
    push_socket.connect("tcp://localhost:5558")

    while True:
        task = await pull_socket.recv_json()
        sum_num = sum(task["numbers"])
        num_id = task["num_id"]
        print(f"{sum_num=}")

        result = {
            "worker_id": worker_id,
            "num_id": task["num_id"],
            "partial_sum": sum_num,
        }

        print(f"{worker_id=} {num_id=} {sum_num=}")
        await push_socket.send_json(result)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: worker.py id")
        exit(1)

    asyncio.run(worker(sys.argv[1]))
