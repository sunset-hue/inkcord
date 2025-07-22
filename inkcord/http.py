import http
import http.client
import asyncio
import typing
import json

class Request:
    def __init__(self,method: typing.Literal['POST','GET','PUT','DELETE','PATCH'],data: dict):
        self.method = method
        self.data = json.dumps(data)






class AsyncHttpClient:
    """This is the basis for http interactions."""
    def __init__(self,token: str,version: int = 10):
        self.headers = {
            "User-Agent": "DiscordBot (https://github.com/inkcord,0.1.0a)",
            "Content-Type": "application/json",
            "Authorization": f"Bot {token}"
        }
        self.path: str = f"https://discord.com/api/v{version}"
    
    
    async def send_multiple_requests(self, *requests: Request):
        """Lowest level interface in this library to send and recieve the result of multiple requests.
        :param requests: The list of requests to send and recieve the result of.
        :type requests: inkcord.Request
        :returns: List[asyncio.Future] -- The result of the requests
        :raises: Exception placeholder"""
        