import asyncio

ORDERS = [
    ("O-1001", 42.00),
    ("O-1002", 15.50),
    ("O-1003", 88.00),
    ("O-1004", 23.25),
    ("O-1005", 61.10),
]


async def charge_card(order_id, amount, attempt):
    await asyncio.sleep(0)
    print(f"charged ${amount} for {order_id}")
    if order_id == "O-1003" and attempt == 1:
        print(f"no confirmation for {order_id} (dropped)")
        return False
    return True


async def order_flow(order_id, amount):
    print(f"received order {order_id} for ${amount}")
    ok = await charge_card(order_id, amount, attempt=1)
    if not ok:
        print("no confirmation, retrying charge...")
        await charge_card(order_id, amount, attempt=2)
    print(f"order {order_id} complete")


async def main():
    await asyncio.gather(
        *(order_flow(oid, amt) for oid, amt in ORDERS)
    )


asyncio.run(main())
