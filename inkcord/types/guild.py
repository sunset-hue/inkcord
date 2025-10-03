import typing

if typing.TYPE_CHECKING:
    from ..resourceid import ResourceID
    from permissions import Permissions
    from .role import Role
    from .emoji import Emoji

class PartialGuild:
    
    def __init__(self,_data: dict):
        self.__data = _data

    
    @property
    def id(self):
        """The partial guild's ID."""
        return ResourceID(self.__data["id"])
    
    @property
    def name(self) -> str:
        """The name of the partial guild."""
        return self.__data["name"]
    
    @property
    def icon(self) -> str:
        """Contains a CDN link to the icon of the partial guild."""
        return f"https://cdn.discordapp.com/icons/{self.id}/{self.__data["icon"]}.png"

    @property
    def banner(self) -> str:
        """Contains a CDN link to the banner of the partial guild."""
        return f"https://cdn.discordapp.com/banners/{self.id}/{self.__data["banner"]}.png"
    
    @property
    def owner(self) -> bool:
        """Whether the current user is the owner of this partial guild."""
        return self.__data["owner"]
    
    @property
    def permissions(self) -> Permissions:
        return Permissions(self.__data["permissions"])
    
    @property 
    def features(self) -> list[str]:
        return self.__data["features"]
    
    @property
    def approx_member_count(self) -> int | None:
        """The approximate member count."""
        return self.__data.get("approximate_member_count")

    @property
    def approx_presence_count(self) -> int | None:
        """The approximate presence count of the guild."""
        return self.__data.get("approximate_prescence_count")


class Guild:
    "A representation of the Guild object defined in the discord gateway."
    # oh no this is gonna be a ton of work T_T
    def __init__(self,_data):
        self.__data = _data
        
    
    @property
    def id(self):
        "The guild's id."
        return ResourceID(self.__data["id"])
    
    @property
    def name(self) -> str:
        "The name of the guild."
        return self.__data["name"]
    
    @property
    def icon(self):
        "CDN link leading to the icon of the guild."
        return f"https://cdn.discordapp.com/icons/{self.id}/{self.__data["icon"]}.png" if self.__data["icon"] is not None else None
    
    @property
    def splash(self):
        "CDN link leading to the guild's splash banner."
        return f"https://cdn.discordapp.com/splashes/{self.id}/{self.__data["splash"]}.png" if self.__data["splash"] is not None else None
    
    @property
    def owner(self) -> bool | None:
        "Whether the bot is the owner of the guild."
        return self.__data.get("owner")
    
    
    @property
    def owner_id(self) -> ResourceID:
        "The ID of the owner of the guild."
        return ResourceID(self.__data["owner_id"])
    
    @property
    def permissions(self) -> Permissions:
        """Permissions for the specific user in the guild."""
        return Permissions(self.__data["permissions"])
        # this is a placeholder for now
    
    @property
    def afk_channel_id(self) -> ResourceID | None:
        """AFK channel id."""
        return ResourceID(self.__data["afk_channel_id"]) if self.__data.get("afk_channel_id") else None
    
    @property
    def afk_timeout(self) -> int:
        """The AFK timeout in seconds."""
        return self.__data["afk_timeout"]

    @property
    def widget_enabled(self) -> bool | None:
        """Whether the server widget is enabled."""
        return self.__data.get("widget_enabled")
    
    @property
    def widget_channel_id(self) -> ResourceID | None:
        """The ID of the widget channel."""
        return ResourceID(self.__data["widget_channel_id"]) if self.__data.get("widget_channel_id") else None
    
    @property
    def verification_level(self) -> int:
        """Verification level of the guild.
        0 - unrestricted
        1 - must have a verified email on the account.
        2 - must be registered on discord for longer than 5 minutes.
        3 - must be registered on discord for longer than 10 minutes.
        4 - must have a verified phone number"""
        return self.__data["verification_level"]
    
    @property
    def default_message_notif_level(self) -> int:
        """The default message notification level of the guild.
        1 - only mentions
        2 - all messages"""
        return self.__data["default_message_notifications"]
    
    @property
    def explicit_content_filter(self) -> int:
        """The explicit content filter level of the guild.
        0 - disabled 
        1 - members without roles
        2 - all members"""
        return self.__data["explicit_content_filter"]
        
    
    @property
    def roles(self) -> list[Role]:
        """All the roles in the guild."""
        return [Role(data) for data in self.__data["roles"]]
    
    @property
    def emojis(self) -> list[Emoji]:
        """All the emojis in the guild."""
        return [Emoji(data) for data in self.__data["emojis"]]
    
    @property
    def mfa_level(self) -> int:
        """The MFA level of this guild (multi factor authentication)
        can be one of 2 values:
        None - 0
        Elevated - 1"""
        return self.__data["mfa_level"]