"""
Copyright © 2025 sunset-hue

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""



import http
import http.client as httcl
import asyncio
import typing
import json
import logging
import websockets
import platform
from enums import BitIntents, RESUMABLE_CLOSE_CODES
import threading
from .thread_owning import handle_events,GatewayEvent
from .listener import EventListener
from .exceptions import RequestException


logger = logging.getLogger("inkcord-establish")
formatter = logging.Formatter("[ \x1b[38;2;255;128;0m \x1b[3;1m%(name)s-gateway_handler] | %(levelname)s \x1b[0m ~\x1b[38;2;255;217;0m \x1b[4;1m%(asctime)s~: %(message)s",datefmt="%a %H:%M")
class Request:
    def __init__(self,method: typing.Literal['POST','GET','PUT','DELETE','PATCH'],data: dict,route: str):
        self.method = method
        self.data = json.dumps(data)
        self.api_route = route
        # this owner field is to organize which thread is responding to which event


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
        # this loop is going to be used by (almost) all other routines so the lib is effectively async
    
    
    @classmethod
    def setup(cls,token: str,intents: int,version: int = 10,gateway: bool = True,event_listners: list[EventListener] | None = None):
        """ A class method that does the gateway setup.
        """
        class_setup = cls(token,intents,version,gateway)
        class_setup.get_gateway_url()
        class_setup.event_listeners = event_listners
        return class_setup
    
    
    def send_multiple_requests(self, *requests: Request):
        """Lowest level interface in this library to send and recieve the result of multiple requests.
        :param requests: The list of requests to send and recieve the result of.
        :type requests: inkcord.Request
        :returns: List[asyncio.Future] -- The result of the requests
        :raises: Exception placeholder
        NOTE: Don't use this function unless necessary, there are much simpler ways to send requests."""
        futures: list[asyncio.Future] = []
        for request in requests:
            self.loop.run_in_executor(None,self.http_connection.request,request.method,f"{self.path}{request.api_route}",request.data,self.headers)
            # this also needs to run in an executor so it's also multithreaded and isn't blocking
            current_future = self.loop.run_in_executor(None,self.http_connection.getresponse)
            futures.append(current_future)
            # absolutely no idea if the *args argument is for the func or not
        return futures
    
    def send_request(self,method: typing.Literal['POST','GET','PUT','DELETE','PATCH'],route: str,data: dict | None):
        """Lowest level interface in this library to send and recieve the result of a request
        :param method: The method to send to the discord API
        :type method: Literal['POST','GET','PUT','DELETE','PATCH']
        :param route: The route to send the request to. Has to be valid.
        :type route: str
        :param data: A dictionary containing the information that you're sending with the request.
        :type data: dict[str,Any]
        :returns: asyncio.Future
        :raises: RequestException
        NOTE: Don't use this function unless necessary, there are much simpler ways to send requests.
        """
        if method == "GET":
            self.loop.run_in_executor(None,self.http_connection.request,method,f"{self.path}{route}",None,self.headers)
        else:
            request_to_check = self.loop.run_in_executor(None,self.http_connection.request,method,f"{self.path}{route}",data)
            result_to_check = self.loop.run_in_executor(None,self.http_connection.getresponse)
            if result_to_check.result().getcode() >= 200:
                raise RequestException("send_request(): Raised RequestException due to response code being above 200, indicating an error. Check authentication or to make sure that the request body is not malformed.")
            else:
                return result_to_check 
    
    def get_gateway_url(self):
        url = self.send_request('GET',"gateway",None)
        url_response = url.result()
        url_unwrap: dict[str,str] = json.loads(url_response.msg.as_string())
        self.gate_url: str | None = url_unwrap["url"]
    
    async def send_heartbeat(self,serialized_data: dict,gateway: websockets.ClientConnection):
        try:
            if serialized_data["op"] == 11:
                await asyncio.sleep(self.interval / 1000)
                await gateway.send(json.dumps({ "op": 1,"d": self.s if self.s > 0 else None }))
                logger.info("Heartbeat sent.")
            # this is temporary, to make sure it's sending the heartbeats correctly
            elif serialized_data["op"] == 1:
                await gateway.send(json.dumps({ "op": 1,"d": self.s if self.s > 0 else None }))
                logger.info("Heartbeat sent immediately.")
        except (websockets.exceptions.ConnectionClosedError,websockets.exceptions.ConnectionClosedOK) as e:
            if isinstance(e,websockets.exceptions.ConnectionClosedError):
                logger.error("Connection was closed. Attempting reconnect....")
    
    async def thread_handler(self,loop: asyncio.AbstractEventLoop):
            thread = threading.Thread(None,handle_events,None,(loop,self.event_listeners,logger,self.gateway_conn))
            thread.start()
            # this is placeholder code for now, it's gonna manage all the thread queue stuff soon
    
    
    
    async def establish_queue_handshake(self):
        logger.info("Handshake routine was successfully called. Initiating handshake...")
        gateway = await websockets.connect(self.gate_url)
        self.gateway_conn = gateway
        event_queue = []
        async for message in gateway:
            serialized_data = json.loads(message)
            try:
                if serialized_data["op"] == 10:
                    self.interval = serialized_data["d"]["heartbeat_interval"]
                await self.send_heartbeat(serialized_data,gateway)
                logger.info(f"Initiated heartbeat at {self.interval}ms.")
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
                await self.establish_queue_handshake()
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
                await self.establish_queue_handshake()
                # this may or may not cause recursion
            
        