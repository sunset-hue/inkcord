from typing import Any
from .http_gateway import logger

class RequestException(Exception):
    def __init__(self,*args):
        logger.fatal(args)
    # doesn't need any extra implementation here, don't need to handle anything

        