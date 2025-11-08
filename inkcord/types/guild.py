import typing
import json
from typing import Self
import PIL.Image
import base64
from typing import overload


if typing.TYPE_CHECKING:
    from ..resourceid import ResourceID
    from permissions import Permissions
    from .role import Role
    from .emoji import Emoji
    from ..shared_types import WelcomeScreen, Sticker
    from .channel import Channel, VoiceChannel
    from ..exceptions import ImproperUsage


class PartialGuild:

    def __init__(self, _data: dict):
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
        return (
            f"https://cdn.discordapp.com/banners/{self.id}/{self.__data["banner"]}.png"
        )

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
    def __init__(self, _data):
        self.__data = _data

    def __str__(self):
        return self.name

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
        return (
            f"https://cdn.discordapp.com/icons/{self.id}/{self.__data["icon"]}.png"
            if self.__data["icon"] is not None
            else None
        )

    @property
    def splash(self):
        "CDN link leading to the guild's splash banner."
        return (
            f"https://cdn.discordapp.com/splashes/{self.id}/{self.__data["splash"]}.png"
            if self.__data["splash"] is not None
            else None
        )

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
        return (
            ResourceID(self.__data["afk_channel_id"])
            if self.__data.get("afk_channel_id")
            else None
        )

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
        return (
            ResourceID(self.__data["widget_channel_id"])
            if self.__data.get("widget_channel_id")
            else None
        )

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

    @property
    def application_id(self) -> ResourceID | None:
        """The App ID of the app that created the guild, if applicable."""
        return (
            ResourceID(self.__data.get("application_id"))
            if self.__data.get("application_id")
            else None
        )

    @property
    def system_channel_id(self) -> ResourceID | None:
        """System channel ID, if applicable."""
        return (
            ResourceID(self.__data.get("system_channel_id"))
            if self.__data.get("system_channel_id")
            else None
        )

    @property
    def rules_channel_id(self) -> ResourceID | None:
        """Rules channel id, if applicable."""
        return (
            ResourceID(self.__data.get("rules_channel_id"))
            if self.__data.get("rules_channel_id")
            else None
        )

    @property
    def max_presences(self) -> int | None:
        """The number of presences in this guild. Assume this to be always none aside from the largest guilds."""
        return self.__data.get("max_presences")

    @property
    def max_members(self) -> int | None:
        """The cap for the max members in this guild."""
        return self.__data.get("max_members")

    @property
    def vanity_url(self) -> str | None:
        """The vanity URL for this guild."""
        return f"https://discord.gg/{self.__data.get("vanity_url_code")}"

    @property
    def description(self) -> str | None:
        """The description of the guild."""
        return self.__data.get("description")

    @property
    def banner(self) -> str | None:
        """The CDN link for the guild banner."""
        return (
            f"https://cdn.discordapp.com/banners/{self.id}/{self.__data.get("banner")}"
            if self.__data.get("banner")
            else None
        )

    @property
    def premium_tier(self) -> int:
        """The premium tier of the guild (server boosts tier). Value ranges from 0 to 3."""
        return self.__data["premium_tier"]

    @property
    def number_boosts(self) -> int:
        """The number of server boosts the guild has. May be None."""
        return self.__data.get("premium_subscription_count")

    @property
    def preferred_locale(self) -> str:
        """The preferred locale of the Guild. Available options are listed in the `inkcord.Locales` enum."""
        return self.__data["preferred_locale"]

    @property
    def public_updates_channel_id(self) -> ResourceID:
        """The public update channel ID."""
        return self.__data.get("public_updates_channel_id")

    @property
    def max_video_channel_users(self) -> int | None:
        """Max video channel users."""
        return self.__data.get("max_video_channel_users")

    @property
    def max_stage_channel_users(self) -> int | None:
        """Max stage channel users."""
        return self.__data.get("max_stage_video_channel_users")

    @property
    def approx_member_count(self) -> int | None:
        """Approximate member count of guild. Only returned from certain endpoints."""
        return self.__data.get("approximate_member_count")

    @property
    def approx_presence_count(self) -> int | None:
        """Approximate presence count of guild. Only returned from certain endpoints."""
        return self.__data.get("approximate_presence_count")

    @property
    def welcome_screen(self) -> WelcomeScreen | None:
        """The welcome screen for the guild. Can be None."""
        return (
            WelcomeScreen(self.__data["welcome_screen"])
            if self.__data.get("welcome_screen")
            else None
        )

    @property
    def stickers(self) -> list[Sticker] | None:
        """A list of all the stickers in this guild. May be None."""
        return (
            [Sticker(sticker) for sticker in self.__data["stickers"]]
            if self.__data.get("stickers")
            else None
        )

    @property
    def boost_progress_bar_enabled(self) -> bool:
        """Whether the boost progress bar is enabled."""
        return self.__data["premium_progress_bar_enabled"]

    @property
    def safety_alerts_channel_id(self) -> ResourceID | None:
        """The channel ID where Discord sends safety alerts to in this guild. May be None."""
        return (
            ResourceID(self.__data["safety_alerts_channel_id"])
            if self.__data.get("safety_alerts_channel_id")
            else None
        )

    @classmethod
    def get_guild(cls, bot, id: ResourceID, with_counts: bool = False) -> Self:
        """Gets a guild, and constructs a `inkcord.Guild` object out of it.
        `with_counts` just determines whether to return a member count/presence count in a guild.

        Args:
            bot (inkcord.Client): supposed to be inkcord.Client, not typehinted to prevent circular imports.
            id (inkcord.ResourceID): The id of the guild to retrieve.
            with_counts (bool): Whether to return the fields `approximate_member_count` and `approximate_presence_count` in the resulting guild.
        Returns:
            The guild retrieved. (`inkcord.Guild`)
        """
        request = bot._CONN.send_request("GET", f"guilds/{id}", with_counts=with_counts)
        result = self(
            json.loads(request.result().read())
        )  # shut up python this is fine
        return result

    def modify_guild(
        self,
        bot,
        name: str,
        verification_level: int | None,
        default_message_notif_level: int | None,
        explicit_content_filter: int | None,
        afk_channel_id: int | None | ResourceID,
        afk_timeout: int,
        icon: PIL.Image.Image | None,
        splash: PIL.Image.Image | None,
        discovery_splash: PIL.Image.Image | None,
        banner: PIL.Image.Image | None,
        system_channel_id: int | None | ResourceID,
        system_channel_flags: int,
        rules_channel_id: int | None | ResourceID,
        public_updates_channel_id: int | None | ResourceID,
        preferred_locale: str | None,
        description: str | None,
        premium_progress_bar_enabled: bool,
        safety_alerts_channel_id: int | None | ResourceID,
    ):
        """This function allows you to change all of the modifiable aspects of this guild. Note that this request will fail if one of the parameters requires permissions that this user/bot doesn't have.

        Args:
            bot (inkcord.Bot, not typehinted)
            name (str): The name of the guild.
            verification_level (int | None): An integer that's specified in the documentation for the verification level for this guild.
            default_message_notif_level (int | None): An integer that's specified in the documentation for the message notification level for this guild.
            explicit_content_filter (int | None): An integer that's specified in the documentation for the explicit content filter of the guild.
            afk_channel_id (int | None | ResourceID): The afk channel id of the guild.
            afk_timeout (int): The afk timeout length to be moved to the afk channel, in seconds. can be set to: 60, 300, 900, 1800, 3600
            icon (PIL.Image.Image | None): The icon image for the guild.
            splash (PIL.Image.Image | None): The splash image for the guild.
            discovery_splash (PIL.Image.Image | None): The discovery splash image for the guild (this requires this guild to be discoverable)
            banner (PIL.Image.Image | None): The banner image for the guild.
            system_channel_id (int | None | ResourceID): The system channel id of the guild.
            system_channel_flags (int): The system channel flags represented as a integer representation of a bit field.
            rules_channel_id (int | None | ResourceID): The rules channel id of the guild.
            public_updates_channel_id (int | None | ResourceID): the public updates channel id of the guild.
            preferred_locale (str | None): the preferred locale for this guild.
            description (str | None): The description string for this guild.
            premium_progress_bar_enabled (bool): Whether the boost progress bar in this guild is enabled or not.
            safety_alerts_channel_id (int | None | ResourceID): The safety alerts channel id for the guild.

        Returns:
            inkcord.Guild: The updated guild.
        """
        data = {
            "name": name,
            "verification_level": verification_level,
            "default_message_notifications": default_message_notif_level,
            "explicit_content_filter": explicit_content_filter,
            "afk_channel_id": afk_channel_id,
            "afk_timeout": afk_timeout,
            "icon": (
                f"data:image/png;base64,{base64.b64encode(icon.tobytes()).decode()}"
                if icon
                else None
            ),
            "splash": (
                f"data:image/png;base64,{base64.b64encode(splash.tobytes()).decode()}"
                if splash
                else None
            ),
            "discovery_splash": (
                f"data:image/png;base64,{base64.b64encode(discovery_splash.tobytes()).decode()}"
                if discovery_splash
                else None
            ),
            "banner": (
                f"data:image/png;base64,{base64.b64encode(banner.tobytes()).decode()}"
                if banner
                else None
            ),
            "system_channel_id": system_channel_id,
            "system_channel_flags": system_channel_flags,
            "rules_channel_id": rules_channel_id,
            "public_updates_channel_id": public_updates_channel_id,
            "preferred_locale": preferred_locale,
            "description": description,
            "premium_progress_bar_enabled": premium_progress_bar_enabled,
            "safety_alerts_channel_id": safety_alerts_channel_id,
        }
        res = bot._CONN.send_request(
            "PATCH",
            f"guilds/{self.id}",
            data={x: data[x] for x in data if data[x] is not None},
        )
        return self.__init__(json)

    def get_all_channels(self, bot) -> list[Channel]:
        """Returns all the channels in this Guild.
        the `bot` param should be filled with your current client."""
        res = bot._CONN.send_request("GET", f"guilds/{self.id}/channels", None)
        channel_list = []
        for i in res:
            if Channel.__dict__ == i:
                channel_list.append(Channel(i))
            if VoiceChannel.__dict__ == i:
                channel_list.append(VoiceChannel(i))
        return channel_list

    @overload
    def create_channel(self, bot, type: type[Channel], **kwargs): ...

    @overload
    def create_channel(self, bot, type: type[VoiceChannel], **kwargs): ...

    def create_channel(self, bot, type, **kwargs):
        """Creates a channel in this guild.

        Args:
            bot (not typehinted to prevent circular imports, inkcord.Client)
            type (VoiceChannel | Channel (type, not an instance)): The type of channel to create.
            kwargs: Any (Keyword Arguments): The fields to modify in this newly created channel. To see what fields can be modified, check out the Discord API documentation at `https://discord.com/developers/docs`
        """
        res = bot._CONN.send_request("POST", f"guilds/{self.id}/channels", kwargs)
        if type is Channel:
            return Channel(json.loads(res.result()))
        return VoiceChannel(json.loads(res.result()))

    def modify_channel_positions(
        self,
        bot,
        id: ResourceID,
        position: int | None,
        permissions_inherit: bool | None,
        parent_id: ResourceID | None,
    ):
        """Modifies a certain channel's position in this guild.

        Args:
            bot (inkcord.Client, not typehinted to prevent circular imports)
            id (ResourceID): The id of the channel to edit the position of.
            position (int | None): The posotion to change the channel to.
            permissions_inherit (bool | None): Whether to inherit the permissions of the new parent id, if moving to a new channel category.
            parent_id (ResourceID | None): The new parent id for the channel that is moved.
        """
        data = {
            "id": id,
            "position": position,
            "lock_permissions": permissions_inherit,
            "parent_id": parent_id,
        }
        if all(
            [
                id is None,
                position is None,
                permissions_inherit is None,
                parent_id is None,
            ]
        ):
            raise ImproperUsage(
                f"{self.name}.modify_channel_positions()",
                txt="No arguments were supplied to this API call, so no changes were made.",
            )
        else:
            res = bot._CONN.send_request(
                "PATCH",
                f"guilds/{self.id}/channels",
                {x: data[x] for x in data if data[x] is not None},
            )

    def list_active_thread_members(self):
        "Placeholder"
        pass
    
    def list_guild_members(self):
        
