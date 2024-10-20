import sys
import time

import zmq


def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    while True:
        message = socket.recv()
        print(f"Received request: {message}")
        time.sleep(1)
        socket.send(b"World")


def client():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    for request_num in range(10):
        socket.send(f"Hello-{request_num}".encode())
        message = socket.recv()
        print(f"Received reply {request_num}: {message}")


def main():
    if len(sys.argv) != 2:
        print("Usage: script.py [0/1]")
        print("0 - Run as server")
        print("1 - Run as client")
        return

    if sys.argv[1] == "0":
        print("Running as server...")
        server()
    elif sys.argv[1] == "1":
        print("Running as client...")
        client()


if __name__ == "__main__":
    main()
