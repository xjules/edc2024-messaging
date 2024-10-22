import json
import random
import time

import zmq


def job_dispatcher():
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://*:5557")

    # List of sample jobs
    job_types = ["image_processing", "data_analysis", "report_generation"]
    job_id = 0

    print("Job dispatcher is ready to send jobs...")
    time.sleep(1)  # Give workers time to connect

    while True:
        try:
            # Create a job
            job = {
                "job_id": job_id,
                "type": random.choice(job_types),
                "data": f"data_batch_{job_id}",
                "timestamp": time.time(),
            }

            # Send the job
            socket.send_json(job)
            print(f"Dispatched job {job_id}: {job['type']}")

            job_id += 1
            time.sleep(random.uniform(0.5, 2.0))  # Random delay between jobs

        except KeyboardInterrupt:
            print("\nDispatcher shutting down...")
            break


if __name__ == "__main__":
    job_dispatcher()
