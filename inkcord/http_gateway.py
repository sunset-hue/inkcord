"""
Copyright © 2025 sunset-hue

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""



import http.client as httcl
import psutil
import asyncio
import typing
import json
import os
import logging
import websockets
import platform
import threading
import random
import urllib.parse
    
if typing.TYPE_CHECKING:    
    from .shared_types import BitIntents, RESUMABLE_CLOSE_CODES,logger,ThreadJob, FormatterThreading
    from .thread_owning import GatewayEvent
    from .event_handling import handle_events
    from .listener import EventListener
    from .exceptions import RequestException, GeneralException
handler = logging.StreamHandler()
handler.setFormatter(FormatterThreading("[ \x1b[38;2;255;128;0m \x1b[3;1m%(name)s-gateway_handler] | %(levelname)s \x1b[0m ~\x1b[38;2;255;217;0m \x1b[4;1m%(asctime)s~: %(message)s",datefmt="%A %-I:%-M.%-S"))
logger.addHandler(handler)
class Request:
    def __init__(self,method: typing.Literal['POST','GET','PUT','DELETE','PATCH'],data: dict,route: str):
        self.method = method
        self.data = json.dumps(data)
        self.api_route = route


class AsyncClient:
    """This is the basis for http and gateway interactions."""
    def __init__(self,token: str,intents: int,version: int = 10,gateway: bool = True):
        self.headers = {
            "User-Agent": "DiscordBot (https://github.com/inkcord,0.1.0a)",
            "Content-Type": "application/json",
            "Authorization": f"Bot {token}"
        }
        self.path: str = f"https://discord.com/api/v{version}/"
        self.http_connection = httcl.HTTPSConnection(host=self.path)
        self.http_connection.connect()
        self.loop = asyncio.new_event_loop()
        self.gateway = gateway
        self.gate_url: str | None = None
        self.num_reconnects: int = 0
        self.s: int = 0
        self.interval = 0
        self.token = token
        self.intents = intents
        self.version = version
        self.thread_count = psutil.cpu_count()
        self.slash_cmds = []
        self._debug = True if "debug" in os.listdir("..") else False
        self.pending_reqs = []
        if self.thread_count == 1:
            raise GeneralException("bro how the HELL do you only have 1 thread is ur computer from the 1990s or something idek how this would happen")
        # max amount of threads is limited to amt of cores because i saw it on a stack overflow thing
        # this loop is going to be used by (almost) all other routines so the lib is effectively async
    
    
    @classmethod
    def setup(cls,token: str,intents: int,version: int = 10,gateway: bool = True,event_listners: list[EventListener] | None = None):
        """ A class method that does the gateway setup.
        """
        class_setup = cls(token,intents,version,gateway)
        class_setup.get_gateway_url()
        class_setup.event_listeners = event_listners #pyright: ignore
        return class_setup
    
    
    def send_multiple_requests(self, *requests: Request):
        """Lowest level interface in this library to send and recieve the result of multiple requests."""
        futures: list[asyncio.Future] = []
        for request in requests:
            self.loop.run_in_executor(None,self.http_connection.request,request.method,f"{self.path}{request.api_route}",request.data,self.headers)
            # this also needs to run in an executor so it's also multithreaded and isn't blocking
            current_future = self.loop.run_in_executor(None,self.http_connection.getresponse)
            futures.append(current_future)
            # absolutely no idea if the *args argument is for the func or not
        return futures
    
    def send_request(self,method: typing.Literal['POST','GET','PUT','DELETE','PATCH'],route: str,data: dict | None,**params):
        """Lowest level interface in this library to send and recieve the result of a request"""
        if method == "GET" or method == "DELETE":
            self.loop.run_in_executor(None,self.http_connection.request,method,f"{self.path}{route}{urllib.parse.urlencode(params)}",None,self.headers)
        else:
            request_to_check = self.loop.run_in_executor(None,self.http_connection.request,method,f"{self.path}{route}",data)
            result_to_check = self.loop.run_in_executor(None,self.http_connection.getresponse) # we can ensure there's only one of these
            jsonified = json.loads(result_to_check.result().read())
            self.requests_left = result_to_check.result().headers.getallmatchingheaders("X-Ratelimit-Remaining")[0]
            if result_to_check.result().getcode() == 429:
                logger.warning("Reached ratelimit, checking fields for when to send again.")
                logger.warning(f"Sending pending request(s) in {jsonified["retry_after"]}s.")
                self.retry_after = jsonified["retry_after"]
                self.pending_reqs.append([method,data,route])
                self.loop.run_in_executor(None,self.handle_http_ratelimit)    
            if result_to_check.result().getcode() >= 400:
                raise RequestException("send_request(): Raised RequestException due to response code being above (or equal to) 400, indicating an error. Check authentication or to make sure that the request body is not malformed.")
            if int(self.requests_left.split(":")[1]) < 5:
                logger.warning("!!! Bot may hit ratelimit soon, remaining requests less than 5. !!! Please remove any unnecessary API calls if you want to prevent this from happening.")
            else:
                return result_to_check 
    
    def get_gateway_url(self):
        url = self.send_request('GET',"gateway",None)
        url_response = url.result()  # pyright: ignore[reportOptionalMemberAccess]
        url_unwrap: dict[str,str] = json.loads(url_response.msg.as_string())
        self.gate_url: str | None = url_unwrap["url"]
    
    async def send_heartbeat(self,serialized_data: dict,gateway: websockets.ClientConnection):
            if serialized_data["op"] == 11:
                await asyncio.sleep(self.interval / 1000)
                await gateway.send(json.dumps({ "op": 1,"d": self.s if self.s > 0 else None }))
                logger.debug("Heartbeat sent.")
            # this is temporary, to make sure it's sending the heartbeats correctly
            elif serialized_data["op"] == 1:
                await gateway.send(json.dumps({ "op": 1,"d": self.s if self.s > 0 else None }))
                logger.debug("Heartbeat sent immediately.")
    
    async def send_heartbeat_forever(self,gateway: websockets.ClientConnection):
        while True:
            a = await asyncio.sleep(self.interval / 1000) if self.current_event["op"] != 1 else None # effectively makes sure it doesn't wait if the op is 1 (this might seem chatgpt like but I just need clarification for myself ok T_T)
            if self.current_event["op"] == 11:
                await gateway.send(json.dumps({ "op": 1,"d": self.s if self.s > 0 else None }))
                logger.debug("Heartbeat sent.")
            if self.current_event["op"] == 1:
                await gateway.send(json.dumps({ "op": 1,"d": self.s if self.s > 0 else None }))
                logger.debug("Heartbeat sent immediately.")
                
                
    
    async def queue_logic(self,events: websockets.ClientConnection):
        # manages the amount of threads and what each thread is doing
        self.threadjobs: list[ThreadJob] = []
        job = ThreadJob()
        curr_threads = 0
        async for message in events:
            if len(self.threadjobs) == self.thread_count and [threadjob for threadjob in self.threadjobs if threadjob.finished == False] == len(self.threadjobs):
                logger.warning("All threads are occupied by an event. Priority events will have new threads created for them, while others will have a DELAYED RESPONSE.")
            srlized = json.loads(message)
            if self._debug:    
                logger.debug(f"Initiating event queue and creating a max of {self.thread_count} threads")
            curr_threads += 1
            curr_thread = threading.Thread(target=handle_events,args=(self,job,self.loop,self.event_listeners,logger,self.gateway_conn)) # type: ignore
            job.event = srlized["t"]
            job.name = curr_thread.name # pyright: ignore[reportAttributeAccessIssue]
            self.threadjobs.append(job)
            n = 0
            for job in self.threadjobs:
                if job.finished:
                    self.threadjobs.pop(n)
                n += 1
        # finally finished im guessing I have no idea

    
    
    
    async def establish_handshake(self):
        logger.info("Handshake routine was successfully called. Initiating handshake...")
        gateway = await websockets.connect(self.gate_url) # type: ignore
        self.gateway_conn = gateway
        event_queue = []
        async for message in gateway:
            self.current_event = json.loads(message)
            serialized_data = json.loads(message)
            if self._debug:
                logger.debug(message)
            try:
                if serialized_data["op"] == 10:
                    self.jitter = random.uniform(0,1)
                    self.interval = serialized_data["d"]["heartbeat_interval"] * self.jitter
                logger.info(f"Sending first heartbeat with a jitter of {self.jitter}")
                await self.send_heartbeat(serialized_data,gateway)
                logger.info(f"Initiated heartbeat at {self.interval}ms.")
                self.interval = serialized_data["d"]["heartbeat_interval"]
                self.loop.run_forever()
                self.loop.create_task(self.send_heartbeat_forever(self.gateway_conn)) # this should work, hopefully it doesn't block
                # to reset back to normal heartbeat time
                    # this shouldn't need a while true loop since it checks whether event recieved is a heartbeat or not
                await gateway.send(message=json.dumps({
                        "op": 2,
                        "d": {
                            "token": self.token,
                            "properties": {
                                "os": platform.platform(),
                                "browser": "inkcord",
                                "device": "inkcord"
                            },
                            "compress": False,
                            "intents": self.intents
                        }
                    }))
                logger.info("Sent IDENTIFY packet. Waiting for response...")
                if serialized_data["op"] == 0 and serialized_data['d'].get('v') == self.version:
                    logger.info(f"Successfully connected to discord gateway with session id: {serialized_data["d"]["session_id"]}")
                    self.session_id = serialized_data["d"]["session_id"]
                    self.resume_url = serialized_data["d"]["resume_gateway_url"]
                    self.app_id = serialized_data["d"]["application"]["id"]
                # from here on, the queue stuff is about to start
                event_queue.append(message)
                thread_event = GatewayEvent(
                    serialized_data["op"],
                    serialized_data["d"],
                    serialized_data["s"],
                    serialized_data["t"]
                )
                logger.info("Gateway handshake is finished. Setting up queue...")
                
            except (websockets.exceptions.WebSocketException,websockets.ConnectionClosed) as e:
                if isinstance(e,websockets.exceptions.WebSocketException):
                    logger.error(f"Encountered an exception when initiating handshake. (starting reconnect...) Error: {e.args}")
                if isinstance(e,websockets.ConnectionClosed):
                    logger.warning(f"Gateway connection was closed with code {e.code}. Running reconnection routine to check whether code is resumable...")
                    await self.reconnect(e.code)
                
            
    async def reconnect(self,close_code: int):
        self.num_reconnects += 1
        if self.num_reconnects == 3:
            logger.fatal(f"Tried to reconnect 3 times, failed all of them. Please report this error to the devs by creating an issue with tag `bug-report` at this link: \n https://github.com/sunset-hue/inkcord/issues")    
        gateway = await websockets.connect(self.resume_url)
        async for data in gateway:
            serialized = json.loads(data)
            if close_code not in RESUMABLE_CLOSE_CODES:
                logger.info("Not a resumable code. Reverting back to handshake...")
                await self.establish_handshake()
            if serialized["op"] == 10:
                message = {
                    "op": 6,
                    "d": {
                        "token": self.token,
                        "session_id": self.session_id,
                        "seq": self.s
                    }
                }
                await gateway.send(json.dumps(message))
            if serialized["op"] == 0 and serialized["t"] == "RESUMED":
                logger.info("Successfully RESUMED.")
            if serialized["op"] == 9 and serialized["d"] == False:
                logger.error("Invalid session. Reverting to handshake")
                await self.establish_handshake()
            
    
    async def handle_http_ratelimit(self):
        await asyncio.sleep(self.retry_after)
        for method,data,route in self.pending_reqs:
            self.send_request(method,route,data)
            logger.info("Sending missed request....")
