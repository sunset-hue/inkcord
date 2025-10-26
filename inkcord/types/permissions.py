import typing
from typing import Callable

if typing.TYPE_CHECKING:
    from ..resourceid import ResourceID


class Permissions:
    """This object represents the permissions a certain role/channel has.
    This object can be edited by setting each variable to a bool. Setting it to any number (other than 0) automatically flips that permission to True.
    """

    def __init__(self, perms: str | None):
        """Initializes a Permissions object with all permissions set to False. \n (If there is a permissions integer provided, (not true in most user cases) use the `._permissionize()` function to apply to fields)"""
        self.perm_num = int(perms)
        self.create_instant_invites = False
        """This permission allows you to create invites for your guild. Applies to Text, Voice, and Stage channels."""
        self.kick_members = False
        """This permission allows you to kick members from the guild. Not relevant to channels."""
        self.ban_members = False
        """This permission allows you to ban members from the guild. Not relevant to channels."""
        self.administrator = False
        """WARNING: This permission automatically sets ALL permissions to True. 
        \n Allows you to bypass channel permission overwrites."""
        self.manage_channels = False
        """This permission allows you to edit and manage channels. Applies to Text, Voice, and Stage channels."""
        self.manage_guild = False
        """This permission allows you to edit and manage guild settings. Not relevant to channels."""
        self.add_reactions = False
        """This permission allows you to add/remove reactions to a message. Applies to Text, Voice, and Stage channels."""
        self.view_audit_log = False
        """This permission allows you to view the audit log of the guild. Not relevant to channels."""
        self.priority_speaker = False
        """This permission allows you to become a priority speaker in a voice channel."""
        self.stream = False
        """This permission allows you to stream in a channel. Applies to Voice and Stage channels."""
        self.view_channel = False
        """This permission allows you or another user to view this channel in their guild channel menu, along with viewing messages or joining voice channels. Applies to all channel types (Text, Voice, Stage)"""
        self.send_messages = False
        """This permission allows you or another user to send a message in this channel."""
        self.send_tts = False
        """This permission allows you or another user to use TTS (text to speech) in this channel."""
        self.manage_messages = False
        """This permission allows you or another user to delete other users' messages in this channel."""
        self.embed_links = False
        """This permission, if enabled, allows you or another user's links to be auto-embedded."""
        self.attach_files = False
        """This permission allows you or another user to attach a file to a message/send files by themselves."""
        self.message_history = False
        """This permission allows you or another user to read the channel's message history."""
        self.mention_everyone = False
        """This permission allows you or another user to mention everyone in a channel."""
        self.use_external_emojis = False
        """This permission allows nitro users to send external emojis in a channel."""
        self.view_guild_insights = False
        """This permission allows you or another user to view guild insights."""
        self.connect = False
        """This permission allows you or another user to join a voice channel."""
        self.speak = False
        """This permission allows you or another user to speak in a voice channel."""
        self.mute_members = False
        """This permission allows you or another user in a voice/stage channel."""
        self.deafen_members = False
        """This permission allows you or another user to deafen members in a voice channel."""
        self.move_members = False
        """This permission allows you or another user to move members between voice/stage channels."""
        self.use_vad = False
        """This permission allows you or another user to enable VAD (Voice Activity Detection) in a voice channel."""
        self.change_nickname = False
        """This permission allows you or another user to change their own nickname."""
        self.manage_nicknames = False
        """This permission allows you or another user to change other people's nicknames."""
        self.manage_roles = False
        """This permission allows you or another user to change guild roles."""
        self.manage_webhooks = False
        """This permission allows you or another user to change webhooks."""
        self.guild_expressions = False
        """This permission allows you or another user to edit emojis, stickers, and soundboard sounds for all users in a guild."""
        self.use_app_commands = False
        """This permission allows you or another user to use application commands in a channel. Applies to all types of channels."""
        self.request_to_speak = False
        """This permission allows you or another user to request to speak in a Stage channel. \n
        ### UNDER ACTIVE DEVELOPMENT FROM API CONTRIBUTORS, SUBJECT TO CHANGE"""
        self.manage_events = False
        """This permission allows you or another user to manage events in a guild channel. Applies to Voice and Stage channels."""
        self.manage_threads = False
        """This permission allows you or another user to manage threads in a text channel."""
        self.public_threads = False
        """This permission allows you or another user to create a public thread."""
        self.private_threads = False
        """This permission allows you or another user to create a private thread."""
        self.external_stickers = False
        """This permission allows nitro users to send external stickers in a channel."""
        self.send_messages_threads = False
        """This permission allows you or another user to send a message in a thread."""
        self.use_embedded_activities = False
        """This permission allows you or another user to use an Activity (applications with the `EMBEDDED` flag enabled (use `inkcord.Client.enable()`))"""
        self.moderate_members = False
        """This permission allows you or another user to time out users in a channel."""
        self.soundboard = False
        """This permission allows you to use soundboard sounds in a voice channel."""
        self.create_guild_expressions = None
        """This permission is not available for developers yet (see discord api docs)"""
        self.create_events = None
        """Not available to developers yet."""
        self.external_sounds = False
        """Allows you or another user to use sounds from another server."""
        self.voice_messages = False
        """Allows you or another user to send voice messages."""
        self.send_polls = False
        """Allows you or another user to send poll messages in a text channel."""
        self.external_apps = False
        """Allows you or another user to use apps from their own authenticated app list (user installed bots)"""
        self.pin_messages = False
        """Allows you or another user to pin a message in a text channel."""

    def _permissionize(self):
        n = 0
        for i, v in self.__dict__:
            if isinstance(v, Callable):
                continue
            else:
                if self.perm_num & 1 << n == 1 << n:  # type: ignore
                    setattr(self, i, True)
        return self


class PermissionOverwrite:
    """Shows an overwritten permission that's exclusive to this channel/resource specifically."""

    def __init__(self, _dict: dict):
        self.applicable_id = ResourceID(_dict["id"])
        """The role/user that this overwrite applies to's ID."""
        self.allow = _dict["allow"]
        self.deny = _dict["deny"]
