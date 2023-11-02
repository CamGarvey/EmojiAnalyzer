from io import BytesIO
from typing import Optional, Callable

from pilmoji.source import BaseSource


class FileBaseSource(BaseSource):

    def __init__(self, path_builder: Callable[[str], str]):
        self.path_builder = path_builder

    def get_emoji(self, emoji: str, /) -> Optional[BytesIO]:
        """Retrieves a :class:`io.BytesIO` stream for the image of the given emoji."""
        path = self.path_builder(emoji)
        try:
            with open(path, "rb") as fh:
                return BytesIO(fh.read())
        except:
            print('failed to find', emoji, path)

    def get_discord_emoji(self, id: int, /) -> Optional[BytesIO]:
        raise NotImplementedError