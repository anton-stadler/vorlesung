import time
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Event:
    type: str
    data: dict
    ts: str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))

event_store: list[Event] = []   # append-only!

def place_order(user, item):
    event_store.append(Event("item_added",   {"user": user, "item": item}))

def cancel_order(user, item):
    event_store.append(Event("item_removed", {"user": user, "item": item}))

def get_orders():
    orders = {}
    for e in event_store:
        u = e.data["user"]
        if e.type == "item_added":   orders.setdefault(u, []).append(e.data["item"])
        if e.type == "item_removed": orders[u].remove(e.data["item"])
    return orders

def replay():
    orders = {}
    for e in event_store:
        u = e.data["user"]
        if e.type == "item_added":   orders.setdefault(u, []).append(e.data["item"])
        if e.type == "item_removed": orders[u].remove(e.data["item"])
        print(f"  [{e.ts}] {e.type:14}  {u:6} · {e.data['item']:12}  →  {dict(orders)}")
        time.sleep(0.6)

# --- Live ---
# place_order("Anna", "Margherita")
# place_order("Ben", "Salami")
# cancel_order("Ben", "Salami")
# place_order("Ben", "Funghi")
# event_store
# get_orders()
# replay()
