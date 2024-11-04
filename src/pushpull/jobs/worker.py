import asyncio
import random
import sys

import zmq
import zmq.asyncio


def do_job(job):
    pass


async def worker(worker_id):
    context = zmq.asyncio.Context()
    master_pull = context.socket(zmq.PULL)
    master_pull.connect("tcp://localhost:5557")

    while True:
        job = await master_pull.recv_json()
        do_job(job)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: worker.py id")
        exit(1)

    asyncio.run(worker(sys.argv[1]))


await update_socket.send_json(
    {
        "job_id": job["job_id"],
        "worker_id": worker_id,
        "status": "complete",
    }
)
