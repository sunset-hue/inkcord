class Permissions:
    """This object represents the permissions a certain role/channel has.
    This object can be edited by setting each variable to a bool. Setting it to any number (other than 0) automatically flips that permission to True."""
    def __init__(self,perms: int | None):
        """Initializes a Permissions object with all permissions set to False. \n (If there is a permissions integer provided, (not true in most user cases) use the `._convert()` function to apply to fields)"""
        self.perm_num = perms
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
        """This permissions allows you to add/remove reactions to a message. Applies to Text, Voice, and Stage channels."""
        
        
        