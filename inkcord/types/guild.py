from ..resourceid import ResourceID



class Guild:
    # oh no this is gonna be a ton of work T_T
    def __init__(self,_data):
        self.__data = _data
        
    
    @property
    def id(self):
        "The guild's id."
        return ResourceID(self.__data["id"])
    
    @property
    def name(self):
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
        return self.__data.get("owner")
    
    
    @property
    def owner_id(self) -> ResourceID:
        return ResourceID(self.__data["owner_id"])
    