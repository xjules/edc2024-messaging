import asyncio

import zmq.asyncio


async def main():
    context = zmq.asyncio.Context()
    receiver = context.socket(zmq.PULL)
    receiver.connect("tcp://localhost:5558")

    # Bind to send work to next step
    sender = context.socket(zmq.PUSH)
    sender.bind("tcp://*:5559")

    print("Step-4: ready to pack and hand over...")
    while True:
        # Wait for order
        order = await receiver.recv_json()
        print(f"Step-4: received order: {order}")
        await asyncio.sleep(10)
        print("Step-4: done with ", order["order_id"])
        await sender.send_json(
            {"step": "pack_and_hand_over", "order_id": order["order_id"]}
        )


if __name__ == "__main__":
    asyncio.run(main())
