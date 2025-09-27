import typing
import functools
import json

if typing.TYPE_CHECKING:
    from .shared_types import BitIntents
    from .event_handling import EventListener
    from .http_gateway import AsyncClient
    from .slash_cmd import InteractionCommand



class HttpClient:
    """A class for your discord bot that will ONLY use http interactions."""
    pass

class Client:
    "A class that uses http and websocket interactions."
    def __init__(self,intents: BitIntents,token: str,version: int = 10):
        self.intents = intents
        self.current_interaction: dict = {}
        self.slash_cmds = []
        self.listeners = []
        self._CONN = AsyncClient.setup(token,intents,version = 10,gateway=True,event_listners= self.listeners)
        self.version = version
        """Please don't touch this it'll break your bot"""
    
        # this is the read only part that i described earlier
    
    def listener(self,func: typing.Callable):
        """creates a listener for a specific event that's not handled by the library.
           To create the listener for the specific event, keep the name of the event as the function name. If the event name is not provided in the function name, then one of 2 things will happen:
           - it will search for the name in the decorator function itself 
           - it will derive the event from the arguments provided (only in rare cases where it's obvious and not ambiguous)
        """
        @functools.wraps(func)
        def functiond(**kwargs):
            self.listeners.append(EventListener(func,func.__name__))
    
    
    def command(self, name: str | None,description: str | None,func: typing.Callable):
        """
        Decorator for a slash command to be registered into discord
        """
        cmds = InteractionCommand(func)
        @functools.wraps(func)
        def add_to_list(**kwargs):
            
            cmds.desc = description
            cmds.name = name
            self.slash_cmds.append(cmds)
        return cmds
        # to get chaining so error handling can be used

    async def sync(self):
        connection = self._CONN.setup(self.token,self.intents,self.version,True,self.listeners)
        curr_synced = connection.send_request("GET",f"applications/{self._CONN.app_id}/commands",None)
        synced = json.loads(curr_synced.result().read())
        if len(synced) > len(self.slash_cmds):
            
        # need to get the app id somehow