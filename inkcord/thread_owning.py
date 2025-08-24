"""
Functions to help with handling events in seperate threads

Copyright © 2025 sunset-hue

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import typing
import websockets
import json
import asyncio

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

class ThreadJob:
    def __init__(self):
        self.finished = False
        self.process_time = 0
        self.result = None
        
        

async def handle_events(loop: asyncio.AbstractEventLoop,handlers: list[EventListener],logger: logging.Logger,events: websockets.ClientConnection):
    # I'm going to restructure this into an async generator so we have actual queues for threads instead of just allocating a thread to one thing
    job = ThreadJob()
    async for event in events:
        srlzed = json.loads(event) 
        handler = [i for i in handlers if i.event == srlzed["op"]]
        if len(handler) > 0:
            logger.info(f"Found event listener for event name {srlzed["t"]}. Running routine now...")
            result = loop.run_in_executor(None,handler[0].func)
            if result.result() is not None:
                logger.warning("Do not add return objects to listeners. This may break the event handling system.")
        else:
            yield job
            # _event_handlers = {
            #   "interaction_create":interaction_create,
            #   blah blah blah implement ones that are needed
            # }
            # _event_handlers[srlzed["t"]](job)
            # and some extra stuff here (idk)


async def interaction_create():
    
        
    