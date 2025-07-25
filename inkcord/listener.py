"""
Defines a EventListener class that contains event data.
"""
from .http_gateway import GatewayEvent
from typing import Callable


class EventListener:
    def __init__(self,function: Callable,event: GatewayEvent):
        self.func = function
        self.event = event.op