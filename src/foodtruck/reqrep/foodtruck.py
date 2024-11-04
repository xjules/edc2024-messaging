import time

import zmq

order_id = 0


def do_order(order):
    global order_id
    print("1. Processing the order...")
    order["order_id"] = order_id
    order["order"] = "ok"
    order_id += 1
    time.sleep(1)
    return order


def ingredients(order):
    print("2. Getting ingredients...")
    time.sleep(2)
    order["ing"] = "ok"
    return order


def cook(order):
    print("3. Cooking")
    order["cook"] = "ok"
    time.sleep(3)
    return order


def prepare(order):
    print("4. Packing and handing over")
    order["prepare"] = "ok"
    time.sleep(1)
    return order


def foodtruck():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        order = socket.recv_json()

        print(f"Received order: {order}")
        order = do_order(order)
        order = ingredients(order)
        order = cook(order)
        order = prepare(order)

        socket.send_json(order)


if __name__ == "__main__":
    foodtruck()
