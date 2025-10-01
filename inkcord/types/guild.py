from ..resourceid import ResourceID
from permissions import Permissions


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
    def afk_channel_id(self) -> int:
        """AFK channel id."""
        return self.__data.get("afk_channel_id")