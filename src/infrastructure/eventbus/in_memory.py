from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict

from src.application.contracts.event_bus import EventBus, EventHandler
from src.shared.events import DomainEvent


class InMemoryEventBus(EventBus):
    def __init__(self) -> None:
        self._handlers: DefaultDict[str, list[EventHandler]] = defaultdict(list)

    def publish(self, event: DomainEvent) -> None:
        for handler in self._handlers[event.name]:
            handler(event)

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        self._handlers[event_name].append(handler)
