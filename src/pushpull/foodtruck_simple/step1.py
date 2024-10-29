import asyncio

import zmq.asyncio


async def monitor_order(receiver, customer):
    while True:
        # Wait for order
        order = await receiver.recv_json()
        print(f"Order {order} is ready!")
        response = {"status": "ready", "order_id": order["order_id"]}
        await customer.send_json(response)


async def main():
    context = zmq.asyncio.Context()
    # Connect to receive work from previous step
    customer = context.socket(zmq.REP)
    customer.bind("tcp://*:5555")
    receiver = context.socket(zmq.PULL)
    receiver.connect("tcp://localhost:5559")

    # Bind to send work to next step
    sender = context.socket(zmq.PUSH)
    sender.bind("tcp://*:5556")

    monitor_task = asyncio.create_task(monitor_order(receiver, customer))

    print("Step-1: ready to take order...")
    while True:
        # Wait for order
        order = await customer.recv_json()
        print(f"Step-1: received order: {order}")
        await asyncio.sleep(10)
        print("Step-1: done with ", order["order_id"])
        await sender.send_json({"step": "process_order", "order_id": order["order_id"]})

    await monitor_task


if __name__ == "__main__":
    asyncio.run(main())
