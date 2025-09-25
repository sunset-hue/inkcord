import typing
import functools

if typing.TYPE_CHECKING:
    from .shared_types import BitIntents
    from .event_handling import EventListener
    from .http_gateway import AsyncClient



class HttpClient:
    """A class for your discord bot that will ONLY use http interactions."""
    pass

class Client:
    "A class that uses http and websocket interactions."
    def __init__(self,intents: BitIntents,token: str):
        self.intents = intents
        self.current_interaction: dict = {}
        self.slash_cmds = ...
        self.listeners = []
        self._CONN = AsyncClient.setup(token,intents,version = 10,gateway=True,event_listners= self.listeners)
        """It should be VERY obvious why you shouldn't touch this attribute, but I (sunset-hue) made it read-only just in case"""
    
    def __getattribute__(self, name: str) -> typing.Any:
        if name == "_CONN":
            return ...
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
    
    
    def command(self, name: str | None,description: str | None):
        """
    Decorator for a slash command to be registered into discord
        """
        
        
    # bitintents is placeholder for now
