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
        if len(text) > 2048:
            raise UserWarning(
                f"embed.footer.text: The text contained here exceeds the character limit of a footer text (2048 characters)"
            )
        for i in self.__payloaded["footer"].keys():
            if not self.__payloaded["footer"][i]:
                self.__payloaded["footer"].pop(i)

    def image(
        self,
        url: str,
        proxy_url: str = "",
        height: int | None = None,
        width: int | None = None,
    ):
        """Attaches an image to this embed.

        Args:
            url (str): The URL to use as the image. Only supports http(s) and discord attachments.
            proxy_url (str, optional): A proxied version of `url`. Defaults to "".
            height (int | None, optional): The height of the image. Defaults to None.
            width (int | None, optional): The width. Defaults to None.
        """
        self.__payloaded["image"] = {
            "url": url if url else None,
            "proxy_url": proxy_url if proxy_url != "" else None,
            "height": height if height else None,
            "width": width if width else None,
        }
        for i in self.__payloaded["image"].keys():
            if not self.__payloaded["image"][i]:
                self.__payloaded["image"].pop(i)

    def thumbnail(
        self,
        url: str,
        proxy_url: str = "",
        height: int | None = None,
        width: int | None = None,
    ):
        """Attaches a thumbnail to this embed.

        Args:
            url (str): The URL to use as the thumbnail. Only supports http(s) and discord attachments.
            proxy_url (str, optional): A proxied version of `url`. Defaults to "".
            height (int | None, optional): The height of the thumbnail. Defaults to None.
            width (int | None, optional): The width. Defaults to None.
        """
        self.__payloaded["thumbnail"] = {
            "url": url if url else None,
            "proxy_url": proxy_url if proxy_url != "" else None,
            "height": height if height else None,
            "width": width if width else None,
        }
        for i in self.__payloaded["thumbnail"].keys():
            if not self.__payloaded["thumbnail"][i]:
                self.__payloaded["thumbnail"].pop(i)

    def video(
        self,
        url: str,
        proxy_url: str = "",
        height: int | None = None,
        width: int | None = None,
    ):
        """Attaches a video to this embed.

        Args:
            url (str): The URL to use as the video. Only supports http(s) and discord attachments.
            proxy_url (str, optional): A proxied version of `url`. Defaults to "".
            height (int | None, optional): The height of the video. Defaults to None.
            width (int | None, optional): The width. Defaults to None.
        """
        self.__payloaded["video"] = {
            "url": url if url else None,
            "proxy_url": proxy_url if proxy_url != "" else None,
            "height": height if height else None,
            "width": width if width else None,
        }
        for i in self.__payloaded["video"].keys():
            if not self.__payloaded["video"][i]:
                self.__payloaded["video"].pop(i)

    def provider(self, name: str, url: str):
        """Creates a provider field for this embed.
        Args:
            name (str): The name of the provider.
            url (str): The URL of the provider.
        """
        self.__payloaded["provider"] = {"name": name, "url": url}

    def author(
        self, name: str, url: str = "", icon_url: str = "", proxy_icon_url: str = ""
    ):
        """Creates a author field for this embed.

        Args:
            name (str): The name of the author.
            url (str, optional): The URL of the author.. Defaults to "".
            icon_url (str, optional): The icon URL of the author. Defaults to "".
            proxy_icon_url (str, optional): A proxied version of the `url`. Defaults to "".
        """
        self.__payloaded["author"] = {
            "name": name,
            "url": url if url != "" else None,
            "icon_url": icon_url if icon_url != "" else None,
            "proxy_icon_url": proxy_icon_url if proxy_icon_url != "" else None,
        }
        for i in self.__payloaded["author"]:
            if not self.__payloaded["author"][i]:
                self.__payloaded["author"].pop(i)
