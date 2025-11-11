import typing as t
from dataclasses import dataclass
from typing import Self

if t.TYPE_CHECKING:
    from types.guild import Guild
    from types.channel import Channel
    from types.guild_mem import GuildMember
    from .exceptions import InteractionFailed

    # from types.message import Message


@dataclass
class Interaction:
    channel: "Channel | None | list[Channel]"
    author: "GuildMember | None | list[GuildMember]"
    guild: "Guild | None | list[Guild]"
    _id: int | None
    _token: None | str
    conn: t.Any

    def send(self, content: str, tts: bool = False) -> None:
        """Sends a message as a response to an interaction in a specific channel.

        Args:
            content (str): The message you want to send.
            tts (bool, optional): Whether this message is TTS. Defaults to False.
        """
        try:
            self.conn.send_request(
                "POST",
                f"interactions/{self._id}/{self._token}/callback",
                {"type": 4, "data": {"tts": tts, "content": content}},
            )
        except Exception as e:
            raise InteractionFailed(f"Interaction with ID {self._id} failed.") from e
