import asyncio
import json
import uuid
from datetime import datetime

import zmq
import zmq.asyncio

# Initialize ZMQ context
context = zmq.asyncio.Context()


async def publisher():
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    while True:
        # Simulate incoming document processing request
        doc_id = str(uuid.uuid4())
        document = {
            "id": doc_id,
            "timestamp": datetime.now().isoformat(),
            "status": "new",
            "completed_steps": [],
        }

        print(f"\n[PUBLISHER] New document received: {doc_id}")

        # Publish the document for processing
        message = {"type": "new_document", "payload": document}
        await socket.send_string(json.dumps(message))

        await asyncio.sleep(5)  # Wait before sending next document


async def text_extractor():
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    result_pub = context.socket(zmq.PUB)
    result_pub.bind("tcp://*:5556")

    while True:
        message = json.loads(await socket.recv_string())
        if message["type"] == "new_document":
            doc = message["payload"]
            print(f"[TEXT EXTRACTOR] Processing document: {doc['id']}")

            # Simulate text extraction
            await asyncio.sleep(2)

            # Publish results
            doc["completed_steps"].append("text_extraction")
            result_message = {"type": "text_extracted", "payload": doc}
            await result_pub.send_string(json.dumps(result_message))


async def thumbnail_generator():
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5556")  # Listen for text extraction completion
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    result_pub = context.socket(zmq.PUB)
    result_pub.bind("tcp://*:5557")

    while True:
        message = json.loads(await socket.recv_string())
        if message["type"] == "text_extracted":
            doc = message["payload"]
            print(f"[THUMBNAIL GENERATOR] Processing document: {doc['id']}")

            # Simulate thumbnail generation
            await asyncio.sleep(3)

            # Publish results
            doc["completed_steps"].append("thumbnail_generation")
            result_message = {"type": "thumbnail_generated", "payload": doc}
            await result_pub.send_string(json.dumps(result_message))


async def sentiment_analyzer():
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5556")  # Listen for text extraction completion
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    result_pub = context.socket(zmq.PUB)
    result_pub.bind("tcp://*:5558")

    while True:
        message = json.loads(await socket.recv_string())
        if message["type"] == "text_extracted":
            doc = message["payload"]
            print(f"[SENTIMENT ANALYZER] Processing document: {doc['id']}")

            # Simulate sentiment analysis
            await asyncio.sleep(4)

            # Publish results
            doc["completed_steps"].append("sentiment_analysis")
            result_message = {"type": "sentiment_analyzed", "payload": doc}
            await result_pub.send_string(json.dumps(result_message))


async def results_collector():
    # Create and track subscription sockets
    sockets = []
    for port in [5557, 5558]:  # Thumbnail and sentiment analysis results
        socket = context.socket(zmq.SUB)
        socket.connect(f"tcp://localhost:{port}")
        socket.setsockopt_string(zmq.SUBSCRIBE, "")
        sockets.append(socket)

    # Track document completion
    documents = {}

    # Create tasks for monitoring each socket
    async def monitor_socket(socket):
        while True:
            message = json.loads(await socket.recv_string())
            doc = message["payload"]
            doc_id = doc["id"]

            if doc_id not in documents:
                documents[doc_id] = set()

            documents[doc_id].update(doc["completed_steps"])

            # Check if document processing is complete
            if len(documents[doc_id]) >= 3:  # All steps completed
                print(f"\n[RESULTS COLLECTOR] Document {doc_id} processing completed!")
                print(f"Completed steps: {documents[doc_id]}\n")
                documents.pop(doc_id)

    # Create and wait for all monitoring tasks
    tasks = [monitor_socket(socket) for socket in sockets]
    await asyncio.gather(*tasks)


async def cleanup(tasks):
    """Cleanup function to handle graceful shutdown"""
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    context.term()


async def main():
    """Main function to start all services"""
    # Create tasks for all services
    tasks = [
        asyncio.create_task(publisher()),
        asyncio.create_task(text_extractor()),
        asyncio.create_task(thumbnail_generator()),
        asyncio.create_task(sentiment_analyzer()),
        asyncio.create_task(results_collector()),
    ]

    try:
        # Wait for all tasks to complete (they won't as they're infinite loops)
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("\nShutdown initiated...")
    finally:
        await cleanup(tasks)
        print("Cleanup completed")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown requested...")
