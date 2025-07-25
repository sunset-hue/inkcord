"""
Functions to help with handling events in seperate threads
"""


import logging
from .http_gateway import GatewayEvent
from .listener import EventListener


async def handle_events(handlers: list[EventListener],logger: logging.Logger,event: GatewayEvent):
    for handler in handlers:
        if handler.event == event.op:
            logger.info("Found handler! Running handler...")
            await handler.func(event)
    if event.t == "INTERACTION_CREATE":
        # note: need to place logic here
        ...    
            # this is placeholder for now
    