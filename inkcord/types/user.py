"""Copyright © 2025 sunset-hue

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

from typing import Any, List
from ..resourceid import ResourceID
from .avatar import AvatarDecoration, Nameplate, PrimaryGuild
import json


class User:
    def __init__(self,_data: dict[str,Any]):
        self.__data = _data
        self._locale = _data["locale"]
        self._flags = _data["flags"]
        self._public_flags = _data["public_flags"]
        
        
    
    @property
    def user_id(self) -> ResourceID:
        "The user's id."
        return ResourceID(self.__data["id"]) # pyright: ignore[reportReturnType]
    
    @property
    def username(self) -> str:
        "The user's name."
        return self.__data["username"] # pyright: ignore[reportReturnType]
    
    @property
    def discriminator(self) -> str:
        "User discriminator. Usually 0 for non bot users."
        return self.__data["discriminator"] # pyright: ignore[reportReturnType]
    
    @property
    def global_name(self) -> str | None:
        "The user's display name."
        return self.__data["global_name"] # pyright: ignore[reportReturnType]
    
    @property
    def avatar(self) -> str | None:
        "contains link to the avatar picture of the user."
        return f"https://cdn.discordapp.com/avatars/{self.user_id}/{self.__data["avatar"]}.{"gif" if self.__data["avatar"].startswith("a_") else "png"}"
    
    @property
    def bot(self) -> bool | None:
        "returns whether the user is a bot or not."
        return self.__data.get("bot")
    
    @property
    def system(self) -> bool | None:
        "returns whether the user is a system user or not."
        return self.__data.get("system")
    
    @property
    def mfa(self) -> bool | None:
        "Whether Multi Factor Authentication is enabled on this account."
        return self.__data.get("mfa_enabled")
    
    @property
    def banner(self) -> str | None:
        return f"https://cdn.discordapp.com/banners/{self.user_id}/{self.__data.get("banner")}.{"gif" if self.__data["banner"].startswith("a_") else "png"}" if self.__data.get("banner") else None
    
    @property
    def accent_color(self) -> str | None:
        "Returns accent color in hexadecimal format."
        return hex(self.__data["accent_color"]) if self.__data.get("accent_color") else None
    
    
    @property
    def avatar_decoration(self) -> AvatarDecoration | None:
        "Returns an AvatarDecoration object which contains avatar decoration data, such as the link to it, and the sku id of it."
        return AvatarDecoration(self.__data["avatar_decoration_data"]) if self.__data.get("avatar_decoration_data") else None
    
    @property
    def collectibles(self) -> List[Nameplate] | Nameplate | None:
        "A list/object containing the current nameplates the user has."
        if self.__data.get("collectibles"):
            nameplate = [Nameplate(data) for data in self.__data["collectibles"]]
            return nameplate[0] if len(nameplate) == 1 else nameplate
        return None
    
    @property
    def guild_tag(self) -> PrimaryGuild | None:
        "Metadata for the guild tag."
        return PrimaryGuild(self.__data["primary_guild"]) if self.__data.get("primary_guild") else None
    
    
    async def get_user(self,bot,id: ResourceID):
        """
        Gets a User object from an id.
        :param bot: This param isn't typehinted to prevent circular imports, but this is supposed to be an `inkcord.Client`.
        :param id: The id of the user. Can be an int or a ResourceID.
        """
        request = bot._CONN.send_request("GET",f"users/{id}",None)
        result = json.loads(request.result().read())
        return self.__init__(result)
        # the init is here because just doing self() raised an error   
    
    
    
    