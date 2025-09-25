import typing
from typing import Callable, Coroutine
import functools
import logging
import inspect
import re

if typing.TYPE_CHECKING:
    from .http_gateway import FormatterThreading
    from .exceptions import HandleableException, GeneralException
    from .shared_types import TYPEMAPS

logger = logging.getLogger("inkcord-slash")
handler = logging.StreamHandler()
handler.setFormatter(FormatterThreading("[ \x1b[38;2;255;128;0m \x1b[3;1m%(name)s-slash] | %(levelname)s \x1b[0m ~\x1b[38;2;255;217;0m \x1b[4;1m%(asctime)s~: %(message)s",datefmt="%A %-I:%-M.%-S"))
logger.addHandler(handler)
class InteractionCommand:
    """An interaction command. Only for use for message slash commands, there are seperate classes for other types."""
    def __init__(self):
        self.handlers = []
        self.func: Callable | Coroutine | None = None
        self.name = None
        self.desc = None
        
    
    
    def on_error(self,func: Callable):
        @functools.wraps(func)
        def error_append(**kwargs):
            for name,value in kwargs:
                if not isinstance(value,HandleableException):
                    logger.warning("Not a handleable exception. Reverting to builtin error handlers")
                    break
            self.handlers.append(func)
    
    
    def _jsonify(self):
        """INTERNAL!!!
        jsonifies command data into a payload to be sent to sync with the discord gateway"""
        pattern =re.compile("^[-_'\\p{L}\\p{N}\\p{sc=Deva}\\p{sc=Thai}]{1,32}$",flags=re.UNICODE)
        matches = pattern.match(self.name) if self.name is not None else pattern.match(self.func.__name__) # pyright: ignore[reportOptionalMemberAccess]
        if matches is not None:
            raise GeneralException(f"{self.func.__name__ if self.name is None else self.name}._jsonify(): Name of command contains illegal unicode characters (somehow?). Please check if your function name returns a match with the following regex: {pattern.pattern}")
        dictified = {
            "name": self.name if self.name is not None else self.func.__name__,
            "type": 1,
            "description": self.desc if self.desc is not None else self.func.__doc__,
            "options": self._jsonify_params()
        }
    
    def _jsonify_params(self):
        l = []
        sig = inspect.signature(self.func)
        typedict = {
            str : "STR",
            int : "INT",
            float : "FLOAT",
            bool : "BOOL"
            
        }
        # this is for basic types, the other TYPEMAPS one is for extra discord defined types
        for i in sig.parameters.keys():
            l.append({
                "name": i,
                "description": None, # this is placeholder for rn, too lazy to add parameter specific descriptions
                "type": TYPEMAPS._member_map_[typedict[sig.parameters[i].annotation]],
                # so ugly :pensive:
                "required": sig.parameters[i] is typing.Optional
                # choices is gonna be it's own thing later
                })
        return l