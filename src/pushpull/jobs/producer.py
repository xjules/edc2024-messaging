import asyncio

import zmq
import zmq.asyncio

context = zmq.asyncio.Context()


async def send_jobs(completion_event):
    """Task for sending jobs"""
    push_socket = context.socket(zmq.PUSH)
    push_socket.bind("tcp://*:5557")

    job_id = 0
    while not completion_event.is_set():
        job_id += 1
        await push_socket.send_json({"job_id": job_id})
        print(f"[SENDER] Sent job {job_id}")
        await asyncio.sleep(0.1)  # Small delay between jobs

    print("[SENDER] Stopped sending jobs")


async def receive_completions(completion_event):
    """Task for receiving job completions"""
    done_socket = context.socket(zmq.PULL)
    done_socket.bind("tcp://*:5558")

    jobs_completed = 0
    while jobs_completed < 100:
        completion = await done_socket.recv_json()
        jobs_completed += 1
        print(
            f"[RECEIVER] Job {completion['job_id']} completed by worker {completion['worker_id']}"
        )
        print(f"[RECEIVER] Progress: {jobs_completed}/100")

    print("\n[RECEIVER] All 100 jobs completed!")
    completion_event.set()  # Signal to stop sending jobs


async def main():
    """Main function coordinating all tasks"""
    completion_event = asyncio.Event()

    # Create all tasks
    tasks = [
        asyncio.create_task(send_jobs(completion_event)),
        asyncio.create_task(receive_completions(completion_event)),
    ]

    # Wait for completion event and cleanup
    try:
        await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    finally:
        # Cancel all tasks
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        context.term()


if __name__ == "__main__":
    asyncio.run(main())
