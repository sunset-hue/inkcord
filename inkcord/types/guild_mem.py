# the user object can't be typehinted here because of circular imports :pensive:
import typing
import datetime

if typing.TYPE_CHECKING:
    from ..resourceid import ResourceID
    from ..shared_types import AvatarDecoration


class GuildMember:
    """A representation of the guild member model defined by the discord gateway
    NOTE:
    the `user` attribute of this class is not typehinted to prevent circular imports, until I can find a workaround for this problem.
    """

    def __init__(self, _data):
        self.__data: dict = _data
        self.user = None
        """This attribute isn't typehinted, but automatically filled in by the inkcord.User class."""
        self.guild = None
        """This attribute isn't typehinted, but it's automatically filled in by the inkcord.Guild class."""
        self.flags = _data["flags"]
        """internal"""

    @property
    def nickname(self) -> str | None:
        """The nickname of the guild member."""
        return self.__data.get("nick")

    @property
    def avatar(self) -> str | None:
        """The CDN link that leads to the guild member's avatar, can be None."""
        avatar = (
            f"https://cdn.discordapp.com/{self.guild.id}/users/{self.user.id}/{self.__data["avatar"]}.{"gif" if self.__data["avatar"].startswith("a_") else "png"}"
            if self.__data.get("avatar")
            else None
        )
        return avatar

    @property
    def roles(self) -> list[ResourceID]:
        """A list of role IDs that this user has."""
        return self.__data["roles"]

    @property
    def premium_since(self) -> datetime.datetime | None:
        """A datetime.datetime object that contains the date when the member started boosting the guild. Can be None."""
        return (
            datetime.datetime.fromisoformat(self.__data["premium_since"])
            if self.__data.get("premium_since")
            else None
        )

    @property
    def deaf(self) -> bool:
        """Whether this member is deafened in a voice channel."""
        return self.__data["deaf"]

    @property
    def mute(self) -> bool:
        """Whether this member is muted in a voice channel."""
        return self.__data["mute"]

    @property
    def pending(self) -> bool | None:
        """Whether this member has passed Membership Screening requirements (see Guild documentation in the discord documentation for more)"""
        return self.__data.get("pending")

    @property
    def permissions(self) -> None:
        """Placeholder until permission system is ready..."""
        pass

    @property
    def communication_disabled_until(self) -> datetime.datetime | None:
        """When this member's timeout will expire, can be None."""
        return (
            datetime.datetime.fromisoformat(self.__data["communication_disabled_until"])
            if self.__data.get("communication_disabled_until")
            else None
        )

    @property
    def avatar_decoration(self) -> AvatarDecoration | None:
        """The member's avatar decoration, can be None."""
        return (
            AvatarDecoration(self.__data["avatar_decoration_data"])
            if self.__data.get("avatar_decoration_data")
            else None
        )
