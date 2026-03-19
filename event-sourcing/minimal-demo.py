import code
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Event:
    """Immutable event stored in the event store."""
    event_type:     str # "ADD" or "REMOVE"
    data:           dict      # {"user": str, "product": str}
    timestamp:      str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S")) # timestamp


event_store: list[Event] = []
"""Append-only event store."""


def place_order(user: str, product: str):
    """Adds an order as an event."""
    new_event = Event("ADD", {"user": user, "product": product})
    event_store.append(new_event)


def cancel_order(user: str, product: str):
    """Adds a cancellation as an event."""
    new_event = Event("REMOVE", {"user": user, "product": product})
    event_store.append(new_event)


def _apply_event(orders: dict, event: Event) -> dict:
    """Applies a single event to the current state."""
    if event.event_type == "ADD":
        return _add(orders, event.data)
    if event.event_type == "REMOVE":
        return _remove(orders, event.data)
    raise ValueError(f"Unknown event type: {event.event_type}")


def get_orders(replay_mode: bool = False) -> dict:
    """Computes current state by replaying all events."""
    orders = {}
    for event in event_store:
        orders = _apply_event(orders, event)
        if replay_mode:
            print(f"  {event.timestamp}  {event.event_type:8}  {event.data['user']:6} · {event.data['product']:12}  →  {orders}")
            time.sleep(0.6)    
    return orders


def _add(orders: dict, data: dict) -> dict:
    """Adds an order to the orders dictionary."""
    product = data["product"]
    new_orders = orders.copy()
    if product not in new_orders:
        new_orders[product] = 1
    elif product in new_orders:
        new_orders[product] += 1
    return new_orders


def _remove(orders: dict, data: dict) -> dict:
    """Removes an order from the orders dictionary."""
    product = data["product"]
    new_orders = orders.copy()
    if product in new_orders:
        new_orders[product] -= 1
        if new_orders[product] == 0:
            del new_orders[product]
    return new_orders


def _run_demo():
    """Runs a demo scenario with sample orders."""
    place_order("Anna", "Margherita")
    place_order("Ben",  "Flötzinger")
    cancel_order("Ben", "Flötzinger")
    place_order("Ben",  "Auer")
    cancel_order("Ben", "Flötzinger")   # typo: already cancelled
    print("\nOrders:", get_orders())
    print("\nReplay:")
    get_orders(replay_mode=True)


if __name__ == "__main__":
    interactive = "--interactive" in sys.argv or "-i" in sys.argv
    if interactive:
        print("\nInteractive (event_store, place_order, cancel_order, get_orders). exit() to quit.")
        code.interact(local=locals())
    else:
        _run_demo()