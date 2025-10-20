from ..resourceid import ResourceID
from .permissions import Permissions


class Role:
    """A representation of a role as defined from the discord gateway."""

    def __init__(self, _data: dict):
        self.__data = _data

    @property
    def id(self) -> ResourceID:
        """The ID of the role."""
        return ResourceID(self.__data["id"])

    @property
    def name(self) -> str:
        """The name of the role."""
        return self.__data["name"]

    @property
    def role_colors(self) -> dict:
        """Returns a dict with 3 keys:
        primary_color
        secondary_color
        tertiary_color
        Please note that if tertiary color is enforced, assume the values of each key being these, respectively:
        11127295, 16759788, 16761760 (hex representations are: 0xA9C9FF, 0xFFBBEC, and 0xFFC3A0, respectively)
        Also, assume that secondary and tertiary colors are not present at all times."""
        return self.__data["colors"]

    @property
    def hoisted(self) -> bool:
        """Whether this role is pinned in the user listing."""
        return self.__data["hoist"]

    @property
    def icon(self) -> str | None:
        """Returns a CDN link to the icon hash of the role, may be None."""
        return (
            f"https://cdn.discordapp.com/role-icons/{self.id}/{self.__data["icon"]}"
            if self.__data.get("icon")
            else None
        )

    @property
    def unicode_emoji(self) -> str | None:
        """The unicode emoji that's associated with the role, if any."""
        return self.__data.get("unicode_emoji")

    @property
    def position(self) -> int:
        """The position this role holds in the user listing."""
        return self.__data["position"]

    @property
    def permissions(self):
        """Placeholder"""
        pass

    @property
    def managed(self) -> bool:
        """Whether this role is managed by an integration."""
        return self.__data["managed"]

    @property
    def mentionable(self) -> bool:
        """Whether this role is mentionable."""
        return self.__data["mentionable"]
