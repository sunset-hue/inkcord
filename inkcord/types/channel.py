import typing
import datetime

if typing.TYPE_CHECKING:
    from ..resourceid import ResourceID
    from .permissions import PermissionOverwrite
    from .user import User


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

    @property
    def position(self) -> int | None:
        """The position of this channel in the guild."""
        return self._data["position"] if self._data.get("position") else None

    @property
    def overwrites(self) -> list[PermissionOverwrite] | None:
        """The overwrites that are exclusive to this specific channel."""
        return (
            [
                PermissionOverwrite(overwrite)
                for overwrite in self._data["permission_overwrites"]
            ]
            if self._data.get("permission_overwrites")
            else None
        )

    @property
    def name(self) -> str | None:
        """The name of this channel. May be None."""
        return self._data["name"] if self._data.get("name") else None

    @property
    def topic(self) -> str | None:
        """The channel topic. Can be 4096 characters max on Forum and Media channels, and 1024 for all other channels. May be None."""
        return self._data["topic"] if self._data.get("topic") else None

    @property
    def last_message_id(self) -> ResourceID | None:
        """The most recent message in this channel's ID. May be None, if in a non text channel."""
        return (
            ResourceID(self._data["last_message_id"])
            if self._data.get("last_message_id")
            else None
        )

    @property
    def slowmode(self) -> int | None:
        """The amount of seconds a user/bot has to wait before sending another message. May be None."""
        return self._data.get("rate_limit_per_user")

    @property
    def parent_id(self) -> ResourceID | None:
        """The id of the parent category for a Text Channel, for threads, the id of the text channel this thread was created."""
        return (
            ResourceID(self._data["parent_id"]) if self._data.get("parent_id") else None
        )

    @property
    def last_pin_timestamp(self) -> datetime.datetime | None:
        """A `datetime.datetime` object representing when the last pinned message in this channel was pinned."""
        return (
            datetime.datetime.fromisoformat(self._data["last_pin_timestamp"])
            if self._data.get("last_pin_timestamp")
            else None
        )

    @property
    def message_count(self) -> int | None:
        """The number of messages in this thread."""
        return self._data.get("message_count")

    @property
    def member_count(self) -> int | None:
        """The number of unique members in this thread, automatically stops counting at 50."""
        return self._data.get("member_count")


class DMChannel(Channel):
    """An object that represents a channel in the context of a DM. Inherits from `inkcord.Channel`."""

    def __init__(self, data: dict):
        super().__init__(data)
        self.recipients: "list[User] | User | None" = None
        """The recipients of this Group DM, if applicable."""
        self.icon: str | None = (
            f"https://cdn.discordapp.com/{data["icon"]}.png"
            if data.get("icon")
            else None
        )
        """The icon hash of this Group DM, if applicable."""
        self.owner_id = ResourceID(data["owner_id"]) if data.get("owner_id") else None
        """The id of the owner of the Group DM, if applicable."""
        self.application_id = (
            ResourceID(data["application_id"]) if data.get("application_id") else None
        )
        """The id of the app that made this DM, if applicable."""
        self.managed: bool = (
            data["managed"] if data.get("managed") else None
        )  # pyright: ignore[reportAttributeAccessIssue]
        """Whether this Group DM is managed by an application, if applicable."""


class VoiceChannel(Channel):
    """An object that represents a channel in the context of a call, or a voice channel in a Guild. Inherits from `inkcord.Channel`."""

    def __init__(self, data: dict):
        super().__init__(data)
        self.bitrate: int = data["bitrate"]
        """The bitrate of this voice channel (in bits)"""
        self.user_limit: int = data["user_limit"]
        """The number of users that can be in this voice channel at once."""
        self.rtc_region = (
            ResourceID(data["rtc_region"]) if data.get("rtc_region") else None
        )
        """The voice region ID for the voice channel. May be None."""
        self.video_quality_mode: int = self._data["video_quality_mode"]
        """The video quality mode for this channel. 0 means it's automatically chosen to protect performance, and 1 means 720p."""
