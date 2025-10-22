import typing

if typing.TYPE_CHECKING:
    from ..resourceid import ResourceID


class Channel:
    """An object that represents a channel in any context. This is the class of with the other classes with a suffix of `Channel` inherit from."""

    def __init__(self, data: dict):
        """Creates a channel. Don't use this for creating a channel, it's a internal initialization function."""
        self._data = data

    @property
    def id(self) -> ResourceID:
        """The id of the channel."""
        return ResourceID(self._data["id"])

    @property
    def guild_id(self) -> ResourceID | None:
        """The ID of the guild that has this channel in it, if applicable."""
        return (
            ResourceID(self._data["guild_id"]) if self._data.get("guild_id") else None
        )


class DMChannel(Channel):
    """An object that represents a channel in the context of a DM. Inherits from `inkcord.Channel`."""

    def __init__(self, data: dict):
        super().__init__(data)
        self.recipients = None
        """The recipients of this Group DM, if applicable."""
