import asyncio
import sys

import zmq.asyncio
from ports import PORTS, STEP_NAMES


async def process_step(step_id: int):
    context = zmq.asyncio.Context()

    # Connect to receive work from previous step
    receiver = context.socket(zmq.PULL)
    input_port = PORTS[f"STEP_{step_id-1}"]
    receiver.connect(f"tcp://localhost:{input_port}")

    # Bind to send work to next step
    sender = context.socket(zmq.PUSH)
    output_port = PORTS[f"STEP_{step_id}"]
    sender.bind(f"tcp://*:{output_port}")

    step_name = STEP_NAMES[step_id]
    print(f"Started {step_name} worker...")

    # Simulate different processing times for different steps
    processing_times = {
        0: 1,  # Food truck order processing
        1: 2,  # Getting ingredients
        2: 3,  # Cooking
        3: 1,  # Packing
    }

    while True:
        # Receive work
        order = await receiver.recv_json()
        order_id = order["order_id"]
        print(f"{step_name}: Processing order {order_id}")

        # Simulate work
        await asyncio.sleep(processing_times[step_id])

        # Add step information to order
        order["steps_completed"].append(step_name)

        # Send to next step
        print(f"{step_name}: Completed order {order_id}")
        await sender.send_json(order)


async def main():
    if len(sys.argv) != 2:
        print("Usage: python worker_step.py <step_id>")
        print("step_id: 0-3 (0:food_truck, 1:ingredient_getter, 2:cook, 3:packer)")
        return

    step_id = int(sys.argv[1])
    if step_id not in STEP_NAMES:
        print("Invalid step_id. Must be between 0 and 3")
        return

    await process_step(step_id)


if __name__ == "__main__":
    asyncio.run(main())
