import json
import time

import zmq


def customer():
    context = zmq.Context()
    dealer_socket = context.socket(zmq.DEALER)
    dealer_socket.setsockopt(zmq.IDENTITY, b"customer")
    dealer_socket.connect("tcp://localhost:5556")

    order = {"item": "hotdog"}
    print(f"Sending order {order}")
    dealer_socket.send_multipart([b"", json.dumps(order).encode()])
    [_, msg] = dealer_socket.recv_multipart()
    order = json.loads(msg)
    print(f"{order=}")


if __name__ == "__main__":
    customer()
