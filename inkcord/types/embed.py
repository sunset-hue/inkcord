class Embed:
    """A rich embed, that conforms to the structure as defined in the discord API."""

    def __init__(self, _data: dict):
        self._data = _data

    @classmethod
    def new(cls):
        """This function is the user interface to creating an embed."""
        return cls({})

    def field(self, title: str, content: str, inline: str):
        """Creates a new field in this Embed.

        Args:
            title (str): The title of this field.
            content (str): The content contained in this field of the embed.
            inline (str): Whether this field should be shown as in the same line as corresponding fields, or a different line.
        """
        if len(title) > 256:
            raise UserWarning(
                f"embed.{title}: This field exceeds the limit of characters that are usable in a embed field title. In a future update, this text will be truncated."
            )
        if len(content) > 1024:
            ...
