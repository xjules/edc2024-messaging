import asyncio

id2step = {
    1: "order",
    2: "ingredients",
    3: "cook",
    4: "prepare",
}

work_time = {
    "order": 10,
    "ingredients": 20,
    "cook": 30,
    "prepare": 10,
}

trigger = {
    "customer": "prepare",
    "order": "customer",
    "ingredients": "order",
    "cook": "ingredients",
    "prepare": "cook",
}

next_step = {
    "customer": "order",
    "order": "ingredients",
    "ingredients": "cook",
    "cook": "prepare",
    "prepare": "customer",
}

ports = {
    "customer": 5554,
    "order": 5555,
    "ingredients": 5556,
    "cook": 5557,
    "prepare": 5553,
}

order_id = 0


async def do_order(order):
    global order_id
    print(f"1. Processing {order=}")
    order["order_id"] = order_id
    order["order"] = "ok"
    order_id += 1
    await asyncio.sleep(10)
    return order


async def ingredients(order):
    print(f"2. Getting ingredients {order=}")
    order["ing"] = "ok"
    await asyncio.sleep(20)
    return order


async def cook(order):
    print(f"3. Cooking {order=}")
    order["cook"] = "ok"
    await asyncio.sleep(30)
    return order


async def prepare(order):
    print(f"4. Packing and handing over {order=}")
    order["prepare"] = "ok"
    await asyncio.sleep(10)
    return order


work_func = {
    "order": do_order,
    "ingredients": ingredients,
    "cook": cook,
    "prepare": prepare,
}


async def do_work(worker_name, order):
    return await work_func[worker_name](order)
