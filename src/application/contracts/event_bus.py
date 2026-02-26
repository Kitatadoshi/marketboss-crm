from __future__ import annotations

from typing import Protocol

from src.shared.events import DomainEvent


class EventHandler(Protocol):
    def __call__(self, event: DomainEvent) -> None: ...


class EventBus(Protocol):
    def publish(self, event: DomainEvent) -> None: ...

    def subscribe(self, event_name: str, handler: EventHandler) -> None: ...
