import logging
import websockets
import asyncio
import json
import datetime
import typing

if typing.TYPE_CHECKING:
    from .listener import EventListener
    from .shared_types import ThreadJob




async def interaction_create(bot,job: ThreadJob,payload: dict):
    bot.current_interaction = payload
    job.finished = True
    # it's super simple for now, because we really don't have to do anything except supply this info for the slash cmds and the functions in it will manage
    
    

async def handle_events(bot,job: ThreadJob | None,loop: asyncio.AbstractEventLoop,handlers: list[EventListener],logger: logging.Logger,events: websockets.ClientConnection):
    time1 = datetime.datetime.now()
    # i don't wannt errors here
    async for event in events:
        srlzed = json.loads(event)  
        handler = [i for i in handlers if i.event == srlzed["op"]] # type: ignore
        if len(handler) > 0:
            logger.info(f"Found event listener for event name {srlzed["t"]}. Running routine now...")
            result = loop.run_in_executor(None,handler[0].func)
            if result.result() is not None:
                logger.warning("Do not add return objects to listeners. This may break the event handling system.")
        else:
            _event_handlers = {
            "interaction_create":interaction_create,
            # this is really all that's important (time constrainted)
            }
            if srlzed["t"] == "RATE_LIMITED":
                logger.warning("Encountered a gateway ratelimit for requesting guild members. Please check code for excessive event dispatches.")
            if srlzed["t"] in _event_handlers:
                await _event_handlers[srlzed["t"].lower()](bot,job,srlzed) # pyright: ignore[reportArgumentType]
    time2 = datetime.datetime.now() # interpeter magic
    job.process_time = time2 - time1 # pyright: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue] # this might work idk