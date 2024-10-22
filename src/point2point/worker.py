import json
import sys
import time

import zmq


def worker(worker_id):
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect("tcp://localhost:5557")

    print(f"Worker {worker_id} is ready to receive jobs...")

    while True:
        try:
            # Receive a job
            job = socket.recv_json()

            # Simulate job processing
            print(f"Worker {worker_id} processing job {job['job_id']}: {job['type']}")
            process_time = {
                "image_processing": 2,
                "data_analysis": 1,
                "report_generation": 1.5,
            }.get(job["type"], 1)

            time.sleep(process_time)  # Simulate processing

            print(f"Worker {worker_id} completed job {job['job_id']}")

        except KeyboardInterrupt:
            print(f"\nWorker {worker_id} shutting down...")
            break


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python worker.py <worker_id>")
        sys.exit(1)

    worker_id = sys.argv[1]
    worker(worker_id)
