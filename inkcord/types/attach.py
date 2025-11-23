import typing
import mimetypes


class Attachment:
    """A representation of the `Attachment` object as provieded in the discord documentation."""

    def __init__(self, _data: typing.IO | dict, path: str | None = None):
        __instance_check = lambda: isinstance(_data, dict)
        self.__type = _data
        # it takes in an IO so we can abstract away the File object that libs like discord.py implement, and we can implement special types of stuff later
        self.id = _data.get("id") if __instance_check else None
        """The ID of the attachment."""
        self.file_name: str | typing.Any = (
            _data.name if __instance_check else _data.get("name")
        )
        """The filename of the attached file."""
        self.title: str | None = _data.get("title") if __instance_check else None
        """The title of the file, may be None."""
        self.description: str | None = (
            _data.get("description") if __instance_check else None
        )
        """The description of the file, may be None."""
        self.content_type: str | None = (
            _data.get("content_type")
            if __instance_check
            else mimetypes.guess_type(path)[0]
        )
        """The MIME content type of this file. Note that if a IO object is provided, inkcord tries to guess the type, and if it can't, then it will issue a warning if verbosity level is high enough or ignore."""
        self.size: int | None = (
            _data.__sizeof__() if not __instance_check else _data.get("size")
        )
        """The size of this file, in bytes. is the `.__sizeof__()` attribute of an IO if applicable, else just returns the size retrieved from the dictionary."""
        self.url: str | None = _data.get("url") if __instance_check else None
        """URL of the source file."""
        self.proxy_url: str | None = (
            _data.get("proxy_url") if __instance_check else None
        )
        """Proxied URL of the source file."""
        self.height: int | None = _data.get("height") if __instance_check else None
        """The height of the image this attachment contains, if applicable."""
        self.width: int | None = _data.get("width") if __instance_check else None
        """The width of the image this attachment contains, if applicable."""
        self.duration: int | None = (
            _data.get("duration_secs") if __instance_check else None
        )
        """The duration (in seconds) of this voice message, if applicable."""
        self.waveform: bytearray | None = (
            _data.get("waveform") if __instance_check else None
        )
        """The base64 encoded bytearray containing this voice message's waveform, if applicable."""
