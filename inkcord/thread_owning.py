"""
Functions to help with handling events in seperate threads
"""


import logging
from .http_gateway import GatewayEvent
from .listener import EventListener


async def handle_events(handlers: list[EventListener],logger: logging.Logger,event: GatewayEvent):
    for handler in handlers:
        if handler.event == event.op:
            await handler.func(event)
            # this is placeholder for now
    