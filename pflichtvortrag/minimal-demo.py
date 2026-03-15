import code
import sys
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

def _apply(orders, event, warn_prefix="", print_event=False):
    item, user = event.data["item"], event.data["user"]
    if event.type == "item_added": orders.setdefault(item, []).append(user)
    elif event.type == "item_removed":
        if item in orders and user in orders[item]: orders[item].remove(user)
        elif print_event: print(f"{warn_prefix}⚠️  WARNUNG: '{user}' hat '{item}' nicht bestellt – Event ignoriert")
    return orders

def get_orders(replay_mode=False):
    orders = {}
    prefix = "  " if replay_mode else ""
    for event in event_store:
        _apply(orders, event, warn_prefix=prefix, print_event=replay_mode)
        if replay_mode:
            print(f"  [{event.ts}] {event.type:14}  {event.data['user']:6} · {event.data['item']:12}  →  {dict(orders)}")
            time.sleep(0.6)
    return {item: users for item, users in orders.items() if users}

def _run_demo():
    place_order("Anna", "Margherita")
    place_order("Ben", "Salami")
    cancel_order("Ben", "Salami")
    place_order("Ben", "Funghi")
    cancel_order("Ben", "Salami")   # Typo: schon storniert
    print("\nBestellungen:", get_orders())
    print("\nReplay:")
    get_orders(replay_mode=True)

if __name__ == "__main__":
    interactive = "--interactive" in sys.argv or "-i" in sys.argv
    if interactive:
        print("\nInteraktiv (event_store, place_order, cancel_order, get_orders). exit() zum Beenden.")
        code.interact(local=locals())
    else:
        _run_demo()
