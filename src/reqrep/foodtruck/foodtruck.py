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

    order_id = 0
    while True:
        order = socket.recv_json()
        print(f"Received order: {order}")
        order["order_id"] = order_id
        order_id += 1

        process_order()

        get_ingredients()

        cook()

        pack_and_hand_over()

        # Send notification to the customer
        order["status"] = "complete"
        socket.send_json(order)


if __name__ == "__main__":
    food_truck()
