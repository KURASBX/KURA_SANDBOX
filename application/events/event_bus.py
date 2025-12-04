"""Bus de eventos para arquitectura event-driven (no implementado)"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class DomainEvent:
    event_type: str
    data: dict[str, Any]
    metadata: dict[str, Any] = None


class EventHandler(ABC):
    @abstractmethod
    async def handle(self, event: DomainEvent):
        pass


class EventBus:
    def __init__(self):
        self._handlers: dict[str, list[EventHandler]] = {}

    def subscribe(self, event_type: str, handler: EventHandler):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    async def publish(self, event: DomainEvent):
        handlers = self._handlers.get(event.event_type, [])
        for handler in handlers:
            handler.handle(event)


event_bus = EventBus()
