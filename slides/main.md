---
theme: black
transition: slide
---
# Messaging Systems in Modern Software Architecture

---

## Introduction

- Critical role in building scalable and resilient distributed systems
- Challenges in selecting suitable messaging infrastructure
- Focus on simplifying implementation of effective messaging solutions

---

## Fundamental Concepts

### Asynchronous vs. Synchronous Communication

- **Synchronous**: Sender waits for receiver's response
- **Asynchronous**: Sender continues without waiting

---

### Sync code

```python
import time

def sync_task(task_id):
    print(f"Start task {task_id}")
    time.sleep(2)
    print(f"End task {task_id}")

start = time.time()
   
ync_task(1)
sync_task(2)

end = time.time()
print(f"Total time: {end - start:.2f} seconds")
```

---

## Synchronous Output

```
Start task 1
End task 1
Start task 2
End task 2
Total time: 4.00 seconds
```
---

---

# ZeroMQ: Synchronous vs Asynchronous Messaging

---

## Synchronous Messaging (Request-Reply)

```python
import zmq
import time

def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        message = socket.recv()
        print(f"Received request: {message}")
        time.sleep(1)  # Simulating work
        socket.send(b"World")

def client():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    for request in range(10):
        print(f"Sending request {request}")
        socket.send(b"Hello")
        message = socket.recv()
        print(f"Received reply {request}: {message}")

# Run server in a separate process
```

---

## Synchronous Messaging Output

Server:
```
Received request: b'Hello'
Received request: b'Hello'
...
```

Client:
```
Sending request 0
Received reply 0: b'World'
Sending request 1
Received reply 1: b'World'
...
```

---

## Asynchronous Messaging (Publish-Subscribe)

```python
import zmq
import asyncio
import time

async def publisher():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    while True:
        message = f"Update {int(time.time())}"
        await socket.send_string(message)
        print(f"Published: {message}")
        await asyncio.sleep(1)

async def subscriber():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    while True:
        message = await socket.recv_string()
        print(f"Received: {message}")

# Run both publisher and subscriber
```

---

## Asynchronous Messaging Output

Publisher:
```
Published: Update 1634567890
Published: Update 1634567891
...
```

Subscriber:
```
Received: Update 1634567890
Received: Update 1634567891
...
```

---

## Key Differences

1. **Communication Pattern**: 
   - Sync: Request-Reply (client waits for each response)
   - Async: Publish-Subscribe (publisher sends without waiting, subscribers receive independently)

2. **Flow Control**:
   - Sync: Natural flow control (each request waits for a reply)
   - Async: No built-in flow control (subscribers might miss messages if they're slow)

3. **Use Cases**:
   - Sync: When each message needs a response (e.g., database queries)
   - Async: For real-time updates or broadcasts (e.g., live stock prices)

---

### Push vs. Pull Message Delivery

- **Push**: Server actively sends messages to clients
- **Pull**: Clients request messages from the server

---

## Messaging Patterns

1. Point-to-Point
2. Publish-Subscribe
3. Request-Reply
4. Push-Pull

---

## ZeroMQ: A High-Performance Messaging Library

- Introduction to ZeroMQ
- Key features and advantages
- Python implementation examples

---

## ZeroMQ in Python: Basic Example

```python
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    print(f"Received request: {message}")
    socket.send(b"World")
```

---

## Conclusion

- Recap of key concepts
- Best practices for implementing messaging systems
- Q&A