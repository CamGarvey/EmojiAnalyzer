from io import BytesIO
from typing import Optional
from urllib.error import HTTPError

from src.helpers.emoji_helper import rgi, codepoints

try:
    import requests
    _has_requests = True
except ImportError:
    requests = None
    _has_requests = False

from pilmoji.source import HTTPBasedSource


class NotoColorEmojiSource(HTTPBasedSource):
    def get_emoji(self, emoji: str, /) -> Optional[BytesIO]:
        url = f'https://fonts.gstatic.com/s/e/notoemoji/latest/{rgi(codepoints(emoji))}/emoji.svg'

        _to_catch = HTTPError if not _has_requests else requests.HTTPError

        try:
            response = self.request(url)
            bytesio = BytesIO(response)
            bytesio.seek(0)  # Reset the position to the beginning of the stream
            return bytesio
        except _to_catch:
            pass

    def get_discord_emoji(self, id: int, /) -> Optional[BytesIO]:
        pass

