import typing

if typing.TYPE_CHECKING:
    from .shared_types import BitIntents
    from .event_handling import 



class HttpClient:
    """A class for your discord bot that will ONLY use http interactions."""
    pass

class Client:
    "A class that uses http and websocket interactions."
    def __init__(self,intents: BitIntents):
        self.intents = intents
        self.current_interaction: dict = {}
        
    # bitintents is placeholder for now
