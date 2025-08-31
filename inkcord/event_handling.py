from .shared_types import logger,ThreadJob
import asyncio
import json
import datetime




async def interaction_create(job: ThreadJob):
    

async def handle_events(bot,job: ThreadJob | None,loop: asyncio.AbstractEventLoop,handlers: list[EventListener],logger: logging.Logger,events: websockets.ClientConnection):
    time1 = datetime.datetime.now()
    # i don't wannt errors here
    async for event in events:
        srlzed = json.loads(event)  
        handler = [i for i in handlers if i.event == srlzed["op"]]
        if len(handler) > 0:
            logger.info(f"Found event listener for event name {srlzed["t"]}. Running routine now...")
            result = loop.run_in_executor(None,handler[0].func)
            if result.result() is not None:
                logger.warning("Do not add return objects to listeners. This may break the event handling system.")
        else:
            _event_handlers = {
            "interaction_create":interaction_create,
            }
            await _event_handlers[srlzed["t"].lower()](job) # pyright: ignore[reportArgumentType]
            ...
    time2 = datetime.datetime.now() # interpeter magic
    job.process_time = time2 - time1 # pyright: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue] # this might work idk