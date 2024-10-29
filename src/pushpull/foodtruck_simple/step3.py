import asyncio

import zmq.asyncio


async def main():
    context = zmq.asyncio.Context()
    receiver = context.socket(zmq.PULL)
    receiver.connect("tcp://localhost:5557")

    # Bind to send work to next step
    sender = context.socket(zmq.PUSH)
    sender.bind("tcp://*:5558")

    print("Step-3: ready to cook...")
    while True:
        # Wait for order
        order = await receiver.recv_json()
        print(f"Step-3: received order: {order}")
        await asyncio.sleep(30)
        print("Step-3: done with ", order["order_id"])
        await sender.send_json({"step": "cook", "order_id": order["order_id"]})


if __name__ == "__main__":
    asyncio.run(main())
