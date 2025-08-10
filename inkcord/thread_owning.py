"""
Functions to help with handling events in seperate threads

Copyright © 2025 sunset-hue

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import typing

if typing.TYPE_CHECKING:
    import logging
    from .listener import EventListener

class GatewayEvent:
    def __init__(self,op: int,d: dict, s: int, t: str):
        self.op = op
        self.d = d
        self.s = s
        self.t = t
        self.owner = None


async def handle_events(handlers: list[EventListener],logger: logging.Logger,event: GatewayEvent):
    for handler in handlers:
        if handler.event == event.op:
            logger.info("Found handler! Running handler...")
            await handler.func(event)
    if event.t == "INTERACTION_CREATE":
        # note: need to place logic here
        ...    
            # this is placeholder for now
    