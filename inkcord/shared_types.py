"""
Copyright © 2025 sunset-hue

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import enum
import logging


class BitIntents(enum.IntEnum):
    """The class you should use to edit intents.
    + = add a permission
    - = remove a permission
    There are several methods in this class that provide presets for intents."""

    GUILDS = 1 << 0
    """Adding this allows your bot to recieve: (or send) \n
    - `GUILD_CREATE/UPDATE/DELETE` \n
    - `GUILD_ROLE_CREATE/UPDATE/DELETE` \n
    - `CHANNEL_CREATE/UPDATE/DELETE` \n
    - `CHANNEL_PINS_UPDATE` \n
    - `THREAD_CREATE/UPDATE/DELETE` \n
    - `THREAD_LIST_SYNC` \n
    - `THREAD_MEMBER_UPDATE` and `THREAD_MEMBERS_UPDATE` \n
    - `STAGE_INSTANCE_CREATE/UPDATE/DELETE`"""
    GUILD_MEMBERS = 1 << 1
    """!! PRIVILEGED INTENT !!\n 
    Adding this allows your bot to recieve: (or send) \n
    - `GUILD_MEMBER_ADD/UPDATE/REMOVE` \n
    - `THREAD_MEMBERS_UPDATE`
    """
    GUILD_MODERATION = 1 << 2
    """Adding this allows your bot to recieve: (or send) \n
    - `GUILD_AUDIT_LOG_ENTRY_CREATE` \n
    - `GUILD_BAN_ADD/REMOVE`
    """
    GUILD_EXPRESSIONS = 1 << 3
    """Adding this allows your bot to recieve: (or send) \n
    - `GUILD_EMOJIS_UPDATE` \n
    - `GUILD_STICKERS_UPDATE` \n
    - `GUILD_SOUNDBOARD_CREATE/UPDATE/DELETE` \n
    - `GUILD_SOUNDBOARD_SOUNDS_UPDATE`"""
    GUILD_INTEGRATIONS = 1 << 4
    """Adding this allows your bot to recieve: (or send) \n
    - `GUILD_INTEGRATIONS_UPDATE` \n
    - `INTEGRATION_CREATE/UPDATE/DELETE`"""
    GUILD_WEBHOOKS = 1 << 5
    """Adding this allows your bot to recieve/send this event: `WEBHOOKS_UPDATE`"""
    GUILD_INVITES = 1 << 6
    """Adding this allows your bot to recieve/send these events: \n
    - `INVITE_CREATE/DELETE`"""
    GUILD_VOICE_STATES = 1 << 7
    """Adding this allows your bot to recieve/send these events: \n
    - `VOICE_CHANNEL_EFFECT_SEND` \n
    - `VOICE_STATE_UPDATE`"""
    GUILD_PRESENCES = 1 << 8
    """!! PRIVILEGED INTENT !! 
    \n Adding this allows your bot to recieve/send this event: `PRESENCE_UPDATE`"""
    GUILD_MESSAGES = 1 << 9
    """Adding this allows your bot to recieve/send these events: \n
    - `MESSAGE_CREATE/UPDATE/DELETE` \n
    - `MESSAGE_DELETE_BULK`"""
    GUILD_MESSAGE_REACTIONS = 1 << 10
    """Adding this allows your bot to recieve/send these events: \n
  - `MESSAGE_REACTION_ADD/REMOVE` \n
  - `MESSAGE_REACTION_REMOVE_ALL` \n
  - `MESSAGE_REACTION_REMOVE_EMOJI`"""
    GUILD_MESSAGE_TYPING = 1 << 11
    """Adding this allows your bot to recieve/send this event: `TYPING_START`"""
    DIRECT_MESSAGES = 1 << 12
    """Adding this allows your bot to recieve/send these events: \n
  - `MESSAGE_CREATE/UPDATE/DELETE`
  - `CHANNEL_PINS_UPDATE`"""
    DIRECT_MESSAGE_REACTIONS = 1 << 13
    """Adding this allows your bot to recieve/send these events: \n
  - `MESSAGE_REACTION_ADD/REMOVE` \n
  - `MESSAGE_REACTION_REMOVE_ALL` \n
  - `MESSAGE_REACTION_REMOVE_EMOJI`"""
    DIRECT_MESSAGE_TYPING = 1 << 14
    """Adding this allows your bot to recieve/send this event: `TYPING_START`"""
    MESSAGE_CONTENT = 1 << 15
    """!! PRIVILEGED INTENT !! \n
    This intent has no events associated with it, rather it defines what data is sent to specific fields in specific endpoints.
    """
    GUILD_SCHEDULED_EVENTS = 1 << 16
    """Adding this allows your bot to recieve/send these events: \n
    - `GUILD_SCHEDULED_EVENT_CREATE/UPDATE/DELETE` \n
    - `GUILD_SCHEDULED_EVENT_USER_ADD/REMOVE`"""
    AUTOMOD_CONFIG = 1 << 20
    """Adding this allows your bot to recieve/send these events: \n
    - `AUTO_MODERATION_RULE_CREATE/UPDATE/DELETE`"""
    AUTOMOD_EXEC = 1 << 21
    """Adding this allows your bot to recieve/send this event: `AUTO_MODERATION_ACTION_EXECUTION`"""
    GUILD_MESSAGE_POLLS = 1 << 24
    """Adding this allows your bot to recieve/send these events: \n
    - `MESSAGE_POLL_VOTE_ADD/REMOVE`"""
    DIRECT_MESSAGE_POLLS = 1 << 25
    """Adding this allows your bot to recieve/send these events: \n
    - `MESSAGE_POLL_VOTE_ADD/REMOVE`"""

    @classmethod
    def all(cls, self):  # class method isn't really needed but I want cleaner syntax
        """Returns intents with ALL options enabled (NOT RECOMMENDED)"""
        final = 0
        for value in BitIntents._value2member_map_.keys():
            final += value
        return final

    @classmethod
    def default(cls, self):  # returns all privileged intents (that's it)
        return cls.GUILD_MEMBERS + cls.GUILD_PRESENCES + cls.MESSAGE_CONTENT


class RESUMABLE_CLOSE_CODES(enum.IntEnum):
    UNKNOWN = 4000
    UNKNOWN_OP = 4001
    DECODE_ERR = 4002
    SESSION_INVALID = 4003
    AUTH_FAILED = 4004
    ALREADY_AUTHED = 4005
    INVALID_SEQ = 4007
    TIMED_OUT = 4009
    INVALID_SHARD = 4010
    INVALID_INTENTS = 4013


logger = logging.getLogger("inkcord-establish")


class ThreadJob:
    def __init__(self):
        self.finished = False
        self.process_time = 0
        self.result = None
        self.event = None
        self.name = ...


class TYPEMAPS(enum.Enum):
    STR = 3
    INT = 4
    BOOL = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    FLOAT = 10
    ATTACHMENT = 11


class AvatarDecoration:
    def __init__(self, _data):
        self.sku: int = _data["sku_id"]
        self.asset = (
            f"https://cdn.discordapp.com/avatar-decoration-presets/{_data["asset"]}.png"
        )


class WelcomeScreenChannel:
    def __init__(self, _data):
        self.channel_id: int = _data["channel_id"]
        self.description: str = _data["description"]


class WelcomeScreen:
    def __init__(self, _data):
        self.desc = _data["description"]
        self.welcome_screen_channels = [
            WelcomeScreenChannel(data) for data in _data["welcome_channels"]
        ]


class Sticker:
    def __init__(self, _data):
        self.id: int = _data["id"]
        """ID of sticker"""
        self.pack_id: int | None = _data.get("pack_id")
        """For builtin stickers, the ID of the pack this sticker is from."""
        self.name: str = _data["name"]
        """The name of the sticker."""
        self.description: str = _data.get("description")
        """Sticker description. May be None."""
        self.tags = _data["tags"]
        """Autocomplete/suggestion tags for the sticker."""
        self.available: bool | None = _data.get("available")
        """Whether this sticker can be used, can be False due to server boost level downgrading"""
        self.guild_id: int | None = _data.get("guild_id")
        """The guild where this guild id originated from"""
        self.sort_value: int = _data.get("sort_value")
        """This sticker's sort order within it's standard pack, if applicable"""


class FormatterThreading(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.DEBUG:
            self._style._fmt = "[ \x1b[38;2;255;128;0m \x1b[3;1m%(name)s-DEBUG Thread: %(threadName)s] (You are in a testing environment/version of inkcord.) | %(levelname)s \x1b[0m ~\x1b[38;2;255;217;0m \x1b[4;1m%(asctime)s~: %(message)s"
            # this is just so I have extra info to debug with
        else:
            self._style._fmt = "[ \x1b[38;2;255;128;0m \x1b[3;1m%(name)s-gateway_handler] | %(levelname)s \x1b[0m ~\x1b[38;2;255;217;0m \x1b[4;1m%(asctime)s~: %(message)s"
