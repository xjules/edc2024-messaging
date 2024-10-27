---
theme: black
transition: slide
---

- design connected software
- thousands of IETF specs - defining standrat for operating internet such as TCP/IP


zeromq patterns:

Key characteristics and use cases:

Request-Reply


Synchronous communication
One-to-one relationships
Good for RPC-style interactions
Automatic request queuing


Publish-Subscribe


One-to-many relationships
Topic-based filtering
Fire-and-forget messaging
No built-in persistence


Push-Pull


Load balancing
Parallel processing
Pipeline workflows
Fair queuing


Dealer-Router


Async request-reply
Complex routing
Load balancing
Many-to-many relationships


Pair


Exclusive connection between two peers
Bidirectional communication
Useful for inter-thread communication

Additional Features:

All patterns support multiple transport protocols (tcp, ipc, inproc)
Built-in message framing
Automatic reconnection
High water marks for flow control

--- 

Let's do another example and let's do food truck, which demonstrates the necessity of having multiple workers and async messaging system.  Inside the foodtruck we will have the following jobs:
1) Taking order
2) Getting resources like sausages, bread (or whatever the name is)
3) Cooking the food
4) packing the food.

In the first example (in zmq) we will use only request reply model (for step 1.), which will demonstrate that all other steps when sync is not efficient and can break easilly.

Bottlenecks:

Each order blocks the entire system until completion
New orders can't be taken while processing current order
All steps (getting ingredients, cooking, packing) are sequential


Problems:

Long wait times for customers
No parallel processing of different steps
Inefficient use of resources
Poor scalability
Single point of failure


Limitations:

Can't handle multiple orders simultaneously
No way to optimize different stages of food preparation
No separation of concerns between different workers

You'll notice several issues:

Long wait times between orders
Blocking behavior
Inefficient resource usage
Poor customer experience

This implementation will help demonstrate why we need:

Async messaging
Multiple workers
Different messaging patterns for different parts of the system


## bind
Usage: socket.bind("tcp://address:port")
Role: Server-side role (listener).
Purpose: This method makes the socket listen for incoming connections on the specified address and port.
Typical Use Case: Used when you want this socket to act as the "server" in the communication model, making it accessible to multiple connecting sockets.
Requirements: Only one socket can bind to a specific address/port combination per machine; additional attempts to bind to the same address/port will raise an error.
Bind (used with *): "tcp://*:5556" — This allows the socket to accept connections from any network interface on port 5556.


## connect
Usage: socket.connect("tcp://address:port")
Role: Client-side role (connector).
Purpose: This method makes the socket attempt to connect to a socket that’s already listening (via .bind) on the given address and port.
Typical Use Case: Used when you want this socket to act as the "client" in the communication model, which connects to a specific bound socket.
Connect (requires specific IP or hostname): "tcp://localhost:5556" or "tcp://127.0.0.1:5556" — When connecting, you need to specify a concrete address, not a wildcard.

## Multiple publishers


```python
import zmq

context = zmq.Context()

# Proxy to aggregate multiple publishers and broadcast to subscribers
frontend = context.socket(zmq.XSUB)
frontend.bind("tcp://*:5555")  # Publishers connect here

backend = context.socket(zmq.XPUB)
backend.bind("tcp://*:5556")   # Subscribers connect here

# Start the proxy
zmq.proxy(frontend, backend)
```
