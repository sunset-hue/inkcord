import typing
import functools
import json

if typing.TYPE_CHECKING:
    from .shared_types import BitIntents
    from .event_handling import EventListener
    from .http_gateway import AsyncClient
    from .slash_cmd import InteractionCommand
    from .resourceid import ResourceID



class HttpClient:
    """A class for your discord bot that will ONLY use http interactions."""
    pass

class Client:
    "A class that uses http and websocket interactions."
    def __init__(self,intents: BitIntents,token: str,version: int = 10):
        self.intents = intents
        self.current_interaction: dict = {}
        self.slash_cmds: list[InteractionCommand] = []
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
    
    
    def command(self, name: str | None,description: str | None,func: typing.Callable,private: ResourceID | None):
        """
        Decorator for a slash command to be registered into discord.
        :param name: name of slash command to be registered.
        :param description: description of slash command to be registered.
        :param private: the guild ID to register your command to, if applicable.
        """
        cmds = InteractionCommand(func)
        @functools.wraps(func)
        def add_to_list(**kwargs):
            
            cmds.desc = description # type: ignore
            cmds.name = name # type: ignore
            cmds.private = private # type: ignore
            self.slash_cmds.append(cmds)
        return cmds
        # to get chaining so error handling can be used

    async def sync(self):
        connection = self._CONN.setup(self.token,self.intents,self.version,True,self.listeners) # type: ignore
        curr_synced = connection.send_request("GET",f"applications/{self._CONN.app_id}/commands",None)
        synced = json.loads(curr_synced.result().read()) # type: ignore
        if len(synced) < len(self.slash_cmds):
            for cmd in self.slash_cmds:
                if cmd not in synced:
                    if cmd.private is None: # type: ignore
                        connection.send_request("POST",f"applications/{self._CONN.app_id}/commands",json.loads(cmd._jsonify()))
                                                                                        # this is pretty redundant but i'm too lazy to change the _jsonify func
                    else:
                        connection.send_request("POST",f"applications/{self._CONN.app_id}/guilds/{cmd.private}/commands",json.loads(cmd._jsonify())) # type: ignore
                    
        # need to get the app id somehow