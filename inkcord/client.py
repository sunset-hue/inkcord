import typing
import functools
import json

if typing.TYPE_CHECKING:
    from .shared_types import BitIntents
    from .listener import EventListener
    from .http_gateway import AsyncClient
    from .slash_cmd import InteractionCommand
    from .resourceid import ResourceID


class HttpClient:
    """A class for your discord bot that will ONLY use http interactions."""

    pass


class Client:
    "A class that uses http and websocket interactions."

    def __init__(self, intents: BitIntents, token: str, version: int = 10):
        self.intents = intents
        self.current_interaction: dict = {}
        self.slash_cmds: list[InteractionCommand] = []
        self.listeners = []
        self._CONN = AsyncClient.setup(
            token, intents, version=10, gateway=True, event_listners=self.listeners
        )
        self.version = version
        """Please don't touch this it'll break your bot"""

        # this is the read only part that i described earlier

    def listener(self, func: typing.Callable):
        """creates a listener for a specific event that's not handled by the library."""

        @functools.wraps(func)
        def functiond(**kwargs):
            self.listeners.append(EventListener(func, func.__name__))

        return functiond

    def command(
        self,
        name: str | None,
        description: str | None,
        func: typing.Callable,
        private: ResourceID | None,
    ):
        """A decorator for making slash commands.
        The decorated function should take the bot (if in a seperate file, else ignore this instruction),

        Args:
            name (str | None): The name of the command.
            description (str | None): The description of the command.
            func (typing.Callable): The function to be decorated (don't actually fill this in, you're supposed to use it as a decorator)
            private (ResourceID | None): If not None, this slash command is only synced to one guild.

        Returns:
            inkcord.InteractionCommand : The converted function, with extra metadata attached.
        """
        cmds = InteractionCommand(func)

        @functools.wraps(func)
        def add_to_list(**kwargs):

            cmds.desc = description  # type: ignore
            cmds.name = name  # type: ignore
            cmds.private = private  # type: ignore
            self.slash_cmds.append(cmds)
            return cmds

        return add_to_list

        # to get chaining so error handling can be used

    async def sync(self):
        """
        Syncs all commands attached to this bot.

        """
        connection = self._CONN.setup(self.token, self.intents, self.version, True, self.listeners)  # type: ignore
        curr_synced = connection.send_request(
            "GET", f"applications/{self._CONN.app_id}/commands", None
        )
        synced = json.loads(curr_synced.result().read())  # type: ignore
        if len(synced) < len(self.slash_cmds):
            for cmd in self.slash_cmds:
                if cmd not in synced:
                    if cmd.private is None:  # type: ignore
                        connection.send_request(
                            "POST",
                            f"applications/{self._CONN.app_id}/commands",
                            json.loads(cmd._jsonify()),
                        )
                        # this is pretty redundant but i'm too lazy to change the _jsonify func
                    else:
                        connection.send_request("POST", f"applications/{self._CONN.app_id}/guilds/{cmd.private}/commands", json.loads(cmd._jsonify()))  # type: ignore
