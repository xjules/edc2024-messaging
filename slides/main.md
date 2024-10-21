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
- ZeroMQ: A High-Performance Messaging Library

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

Synchronous vs Asynchronous Messaging

---

## Synchronous Messaging (Request-Reply)
- client waits for each response

server:
```python
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        message = socket.recv()
        time.sleep(1)
        socket.send(b"World")
```
client:
```python
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
for request_num in range(10):
    socket.send(f"Hello-{request_num}".encode())
    message = socket.recv()
    print(f"Received reply {request_num}: {message}")

```

---

## Synchronous Messaging Output

Server:
```
Received request: b'Hello-0'
Received request: b'Hello-1'
...
```

Client:
```
Received reply 0: b'World'
Received reply 1: b'World'
...
```

---

## Asynchronous Messaging (Publish-Subscribe)

- publisher sends without waiting, subscribers receive independently

```python
async def publisher():
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    while True:
        message = f"Update {int(time.time())}"
        await socket.send_string(message)
        print(f"Published: {message}")
        await asyncio.sleep(1)

async def subscriber():
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    while True:
        message = await socket.recv_string()
        print(f"Received: {message}")
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

### Channels (Topics) in ZeroMQ

- In ZeroMQ, channels are often implemented using topics
- Publishers can send messages on different topics
- Subscribers can subscribe to specific topics
- Allows for more granular control over message routing

---

### Endpoints in ZeroMQ

- Strings that define where to bind or connect sockets
- Can use different protocols (tcp, ipc, inproc)
- Allow for flexible network configurations
- Examples:
  - tcp://*:5555 (bind to all interfaces)
  - tcp://localhost:5555 (connect to localhost)
  - ipc:///tmp/feeds (use IPC on Unix systems)

---

### Multi-channel Publisher
```python
async def publisher():
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    channels = ["sports", "weather", "news"]

    while True:
        channel = random.choice(channels)
        message = f"{channel} update at {time.time()}"
        await socket.send_string(f"{channel} {message}")
        print(f"Published: {message}")
        await asyncio.sleep(1)

```

---

### Multi-channel Subscriber
```python
async def subscriber(channels):
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    
    for channel in channels:
        socket.setsockopt_string(zmq.SUBSCRIBE, channel)
    
    while True:
        message = await socket.recv_string()
        print(f"Received: {message}")
```

---

### Multiple Endpoints Example
```python
async def multi_endpoint_publisher():
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.PUB)
    
    socket.bind("tcp://*:5555")
    socket.bind("ipc:///tmp/feeds")
    
    while True:
        message = "Update for all endpoints"
        await socket.send_string(message)
        print(f"Published: {message}")
        await asyncio.sleep(1)
```

### Connect to Multiple Endpoints
```python
async def multi_endpoint_subscriber():
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.SUB)
    
    socket.connect("tcp://localhost:5555")
    socket.connect("ipc:///tmp/feeds")
    
    socket.setsockopt_string(zmq.SUBSCRIBE, "")
    
    while True:
        message = await socket.recv_string()
        print(f"Received: {message}")
```

---

### Key points

- Channels (topics) allow for content-based message filtering
- Endpoints provide flexibility in network configuration
- ZeroMQ supports multiple protocols (tcp, ipc, inproc)
- Publishers can publish on multiple channels
- Subscribers can subscribe to multiple channels
- Sockets can bind/connect to multiple endpoints

---
