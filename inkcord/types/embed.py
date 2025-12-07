class Embed:
    """A rich embed, that conforms to the structure as defined in the discord API."""

    def __init__(self, _data: dict = {}, title: str = ""):
        "Don't use this, use the `new` constructor."
        self._data = _data
        self.__payloaded = {"fields": [], "title": title}

    @classmethod
    def new(cls, title: str):
        """This function is the user interface to creating an embed."""
        return cls(title=title)

    def field(self, name: str, content: str, inline: bool = False):
        """Creates a new field in this Embed.

        Args:
            name (str): The name of this field.
            content (str): The content contained in this field of the embed.
            inline (bool): Whether this field should be shown as in the same line as corresponding fields, or a different line. Defaults to False.
        """
        if len(name) > 256:
            raise UserWarning(
                f"embed.{name}: This field exceeds the limit of characters that are usable (256) in a embed field name. In a future update, this text will be truncated."
            )
        if len(content) > 1024:
            raise UserWarning(
                f"embed.{content}: This field exceeds the limit of characters (1024) that are usable in a embed field content string. In a future update, this text will be truncated."
            )
        self.__payloaded["fields"].append(
            {"name": name, "content": content, "inline": inline}
        )

    def footer(
        self,
        text: str = "",
        icon_url: str | None = None,
        proxy_icon_url: str | None = None,
    ):
        """Creates a footer for this embed.

        Args:
            text (str, optional): The text to put in this footer. Defaults to "".
            icon_url (str | None, optional): The URL of the footer icon. Only supported protocols are (http, https) or attachments. Defaults to None.
            proxy_icon_url (str | None, optional): A proxied URL of the footer icon. Defaults to None.
        """
        self.__payloaded["footer"] = {
            "text": text if text != "" else None,
            "icon_url": icon_url if icon_url else None,
            "proxy_icon_url": proxy_icon_url if proxy_icon_url else None,
        }
        for i in self.__payloaded["footer"].keys():
            if not self.__payloaded["footer"][i]:
                self.__payloaded["footer"].pop(i)
