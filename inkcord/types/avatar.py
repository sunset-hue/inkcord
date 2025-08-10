"""Contains type definitions for the User object"""



class AvatarDecoration:
    def __init__(self,_data):
        self.asset = f"https://cdn.discordapp.com/avatar-decoration-presets/{_data["avatar_decoration_data"]}.png"
        self.sku = _data["sku_id"]
    
class Nameplate:
    ...