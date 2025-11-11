import typing as t
from dataclasses import dataclass

if t.TYPE_CHECKING:
    from types.guild import Guild
    from types.channel import Channel
    from types.guild_mem import GuildMember

    # from types.message import Message


@dataclass
class Interaction:
    channel: "Channel | None | list[Channel]"
    author: "GuildMember | None | list[GuildMember]"
    guild: "Guild | None | list[Guild]"
