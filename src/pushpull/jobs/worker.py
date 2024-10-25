import asyncio
import random
import sys

import zmq
import zmq.asyncio

context = zmq.asyncio.Context()


async def worker(worker_id):
    """Worker that processes jobs"""
    work_socket = context.socket(zmq.PULL)
    work_socket.connect("tcp://localhost:5557")

    done_socket = context.socket(zmq.PUSH)
    done_socket.connect("tcp://localhost:5558")

    while True:
        job = await work_socket.recv_json()

        # Simulate work
        process_time = random.uniform(1, 8)
        await asyncio.sleep(process_time)
        print(f"{worker_id=} done with {job['job_id']=}")

        await done_socket.send_json(
            {
                "job_id": job["job_id"],
                "worker_id": worker_id,
                "process_time": process_time,
            }
        )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: worker.py id")
        exit(1)

    asyncio.run(worker(sys.argv[1]))
