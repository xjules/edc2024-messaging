import asyncio

import zmq
import zmq.asyncio


async def job_producer():
    context = zmq.asyncio.Context()
    master_push = context.socket(zmq.PUSH)
    master_push.bind("tcp://*:5557")

    while True:
        await master_push.send({"job_id": 12})
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
