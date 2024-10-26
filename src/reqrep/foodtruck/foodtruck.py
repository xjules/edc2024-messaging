import time

import zmq


def process_order():
    print("1. Processing the order...")
    time.sleep(1)


def get_ingredients():
    print("2. Getting ingredients...")
    time.sleep(2)


def cook():
    print("3. Cooking")
    time.sleep(3)


def pack_and_hand_over():
    print("4. Packing and handing over")
    time.sleep(1)


def food_truck():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print("Food truck is ready!")

    while True:
        # Wait for order
        order = socket.recv_json()
        print(f"Received order: {order}")

        take_order()

        get_ingredients()

        cook()

        pack_and_hand_over()
        # Send response
        response = {"status": "ready", "order_id": order["order_id"]}
        socket.send_json(response)


if __name__ == "__main__":
    food_truck()
