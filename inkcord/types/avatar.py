"""Contains type definitions for the User object"""


class AvatarDecoration:
    def __init__(self, _data):
        self.asset = f"https://cdn.discordapp.com/avatar-decoration-presets/{_data["avatar_decoration_data"]}.png"
        self.sku = _data["sku_id"]


class Nameplate:
    def __init__(self, _data):
        self.sku_id = _data["sku_id"]
        self.asset = f"https://cdn.discordapp.com{_data["asset"]}"
        self.pallette = _data["palette"]


class PrimaryGuild:
    def __init__(self, _data):
        self.guild_id = _data["identity_guild_id"]
        self.enabled = _data["identity_enabled"]
        self.tag = _data["tag"]
        self.badge = f"https://cdn.discordapp.com/{_data["badge"]}"
