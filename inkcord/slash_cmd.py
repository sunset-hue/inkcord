from typing import Callable, Coroutine
from .shared_types import logger

class InteractionCommand:
    """An interaction command. Only for use for message slash commands, there are seperate classes for other types."""
    def __init__(self, command: Callable | Coroutine):
        self.handlers = None
        if self.handlers == None:
            logger.fatal("No error handlers specified for slash command, this is the default handler. Traceback above.")
            