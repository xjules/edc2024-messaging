import asyncio

import zmq.asyncio

ports_step = {
    "process_order": 5555,
    "get_ingredients": 5556,
    "cook": 5557,
    "pack_and_hand_over": 5558,
}


async def monitor_update(updates_socket, customer_socket, orders_socket):
    while True:
        order = await updates_socket.recv_json()
        print(f"Got update {order=}")
        if order["step"] != "pack_and_hand_over":
            orders_socket.send_json(order)
        else:
            # Send response to customer
            response = {"status": "ready", "order_id": order["order_id"]}
            await customer_socket.send_json(response)


async def food_truck():
    context = zmq.asyncio.Context()
    # customer interaction
    customer_socket = context.socket(zmq.REP)
    customer_socket.bind("tcp://*:5555")

    # publishing internal orders
    orders_socket = context.socket(zmq.PUB)
    orders_socket.bind("tcp://*:5556")

    # listening on internal updates from workers
    updates_socket = context.socket(zmq.SUB)
    updates_socket.setsockopt_string(zmq.SUBSCRIBE, "")
    updates_socket.bind("tcp://*:5557")

    print("Food truck is ready!")

    monitor_task = asyncio.create_task(
        monitor_update(updates_socket, customer_socket, orders_socket)
    )

    while True:
        # Wait for order
        order = await customer_socket.recv_json()
        print(f"Received order: {order}")
        # publish order
        await orders_socket.send_json(
            {
                "step": "place_order",
                "order_id": order["order_id"],
            }
        )

    await monitor_task


if __name__ == "__main__":
    asyncio.run(food_truck())
