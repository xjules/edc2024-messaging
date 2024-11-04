import random
import time

import zmq


def customer():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    while True:
        order = {"item": "hotdog"}
        socket.send_json(order)
        order = socket.recv_json()

        print(f"Got {order=} after {time.time() - start_time:.1f} seconds")
        time.sleep(1)  # Wait before next order


if __name__ == "__main__":
    customer()
