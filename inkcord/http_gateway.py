import http
import http.client as httcl
import asyncio
import typing
import json
import logging


logger = logging.getLogger("inkcord-establish")
formatter = logging.Formatter("[ \x1b[38;2;255;128;0m \x1b[3;1m%(name)s-handshake]\x1b[0m ~\x1b[38;2;255;217;0m \x1b[4;1m%(asctime)s~: %(message)s",datefmt="%a %H:%M")

class Request:
    def __init__(self,method: typing.Literal['POST','GET','PUT','DELETE','PATCH'],data: dict,route: str):
        self.method = method
        self.data = json.dumps(data)
        self.api_route = route


class AsyncClient:
    """This is the basis for http and gateway interactions."""
    def __init__(self,token: str,version: int = 10,gateway: bool = True):
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
        self.gate_url = None
        # this loop is going to be used by (almost) all other routines so the lib is effectively async
    
    
    @classmethod
    def setup(cls,token: str,version: int = 10,gateway: bool = True):
        """ A class method that does the gateway setup.
        """
        class_setup = cls(token,version,gateway)
        class_setup.get_gateway_url()
    
    
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
        :raises: Exception Placeholder
        NOTE: Don't use this function unless necessary, there are much simpler ways to send requests.
        """
        if method == "GET":
            self.loop.run_in_executor(None,self.http_connection.request,method,f"{self.path}{route}")
        else:
            self.loop.run_in_executor(None,self.http_connection.request,method,f"{self.path}{route}",data)
        return self.loop.run_in_executor(None,self.http_connection.getresponse)
    
    def get_gateway_url(self):
        url = self.send_request('GET',"gateway",None)
        url_response = url.result()
        url_unwrap = json.loads(url_response.msg.as_string())
        self.gate_url = url_unwrap["url"]
    
    def establish_queue_handshake(self):
        ...