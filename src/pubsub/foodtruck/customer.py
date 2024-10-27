import time

import zmq


def customer():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    order_id = 0

    while True:
        # Create order
        order = {"order_id": order_id, "item": "hotdog"}

        print(f"Customer {order_id=}")
        start_time = time.time()

        # Send order and wait for response
        socket.send_json(order)
        response = socket.recv_json()

        print(
            f"Got order {response['order_id']} after {time.time() - start_time:.1f} seconds"
        )
        time.sleep(1)  # Wait before next order
        order_id += 1


if __name__ == "__main__":
    customer()
