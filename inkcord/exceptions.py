from typing import Any
from .http_gateway import logger


class RequestException(Exception):
    def __init__(self, *args):
        logger.fatal(args)

    # doesn't need any extra implementation here, don't need to handle anything


class GeneralException(Exception):
    def __init__(self, *args):
        logger.fatal(args)


class HandleableException(Exception):
    def __init__(self, *args):
        pass

    # this is eventually gonna be an exception that has extra info with it like missing permissions and such


class ImproperUsage(Warning):
    def __init__(self, *args, txt: str):
        logger.warning(f" {args}: {txt}")


class RequiredIntentsMissing(Exception):
    def __init__(self, *args):
        logger.fatal(
            f"{args}: Missing required intents to use this endpoint/retrieve resource."
        )
