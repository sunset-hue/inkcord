import typing
from typing import Callable, Coroutine
import functools
import logging

if typing.TYPE_CHECKING:
    from .http_gateway import FormatterThreading
    from .exceptions import HandleableException

logger = logging.getLogger("inkcord-slash")
handler = logging.StreamHandler()
handler.setFormatter(FormatterThreading("[ \x1b[38;2;255;128;0m \x1b[3;1m%(name)s-slash] | %(levelname)s \x1b[0m ~\x1b[38;2;255;217;0m \x1b[4;1m%(asctime)s~: %(message)s",datefmt="%A %-I:%-M.%-S"))
logger.addHandler(handler)
class InteractionCommand:
    """An interaction command. Only for use for message slash commands, there are seperate classes for other types."""
    def __init__(self, command: Callable | Coroutine):
        self.handlers = []
    
    
    def on_error(self,func: Callable):
        @functools.wraps(func)
        def error_append(**kwargs):
            for name,value in kwargs:
                if not isinstance(value,HandleableException):
                    logger.warning("Not a handleable exception. Reverting to builtin error handlers")
                    break
            self.handlers.append(func)