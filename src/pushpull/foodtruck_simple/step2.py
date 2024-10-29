import asyncio

import zmq.asyncio


async def main():
    context = zmq.asyncio.Context()
    receiver = context.socket(zmq.PULL)
    receiver.connect("tcp://localhost:5556")

    # Bind to send work to next step
    sender = context.socket(zmq.PUSH)
    sender.bind("tcp://*:5557")

    print("Step-2: ready to get ingredients...")
    while True:
        # Wait for order
        order = await receiver.recv_json()
        print(f"Step-2: received order: {order}")
        await asyncio.sleep(20)
        print("Step-2: done with ", order["order_id"])
        await sender.send_json(
            {"step": "get_ingredients", "order_id": order["order_id"]}
        )


if __name__ == "__main__":
    asyncio.run(main())
