import typing

if typing.TYPE_CHECKING:
    from ..resourceid import ResourceID
    from .user import User


class Emoji:
    """A representation of the Emoji object, as defined in the discord gateway."""

    def __init__(self, _data: dict):
        self.__data = _data

    @property
    def id(self) -> ResourceID | None:
        """The ID of the emoji (see discord documentation for more), may be None."""
        return self.__data.get("id")

    @property
    def name(self) -> str | None:
        """The name of the emoji, may be none only in reaction emoji objects."""
        return self.__data.get("name")

    @property
    def roles(self) -> list[ResourceID] | None:
        """What role ID's are allowed to use this emoji."""
        return (
            [
                ResourceID(id)
                for id in self.__data["roles"]
                if self.__data["roles"] is not None
            ]
            if self.__data.get("roles")
            else None
        )
        # this might work

    @property
    def user(self) -> User | None:
        """The user that created this emoji,if any."""
        return User(self.__data["user"]) if self.__data.get("user") != None else None

    @property
    def require_colons(self) -> bool | None:
        """Whether this emoji is required to be wrapped in colons (the only case where this is not true is default discord emojis)"""
        return self.__data.get("require_colons")

    @property
    def managed(self) -> bool | None:
        """Whether this emoji is managed by an integration."""
        return self.__data.get("managed")

    @property
    def animated(self) -> bool | None:
        """Whether this emoji is animated or not."""
        return self.__data.get("animated")

    @property
    def available(self) -> bool | None:
        """Whether this emoji is available, can be false if the server downgrades a level due to lack of server boosts"""
        return self.__data.get("available")
