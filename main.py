import os.path
from abc import abstractmethod
from io import BytesIO
from typing import Optional

import emoji
import json

from PIL import Image

from emoji_analyzer import EmojiAnalyzer
from pilmoji.source import MicrosoftEmojiSource, BaseSource


class FileBaseSource(BaseSource):

    def get_emoji(self, emoji: str, /) -> Optional[BytesIO]:
        """Retrieves a :class:`io.BytesIO` stream for the image of the given emoji."""
        codes = []
        for c in emoji:
            code = f'{ord(c):X}'
            if code == 'FE0F':
                break
            codes.append(code)
        path = f"assets/128/"
        prefix = "emoji_u"
        extension = ".png"

        try:
            full = f"{path}{prefix}{'_'.join(codes)}{extension}"
            with open(full.lower(), "rb") as fh:
                return BytesIO(fh.read())
        except:
            print('failed to find', emoji, full)


    def get_discord_emoji(self, id: int, /) -> Optional[BytesIO]:
        raise NotImplementedError


if __name__ == '__main__':
    result = []

    # emoji_analyzer = EmojiAnalyzer('/Users/camerongarvey/Downloads/NotoColorEmoji.ttf', source=FileBaseSource)
    emoji_analyzer = EmojiAnalyzer('/System/Library/Fonts/Apple Color Emoji.ttc', source=FileBaseSource)

    red, green, blue = emoji_analyzer.get_average_color_text('◼️', show=True)
    for e in emoji.EMOJI_DATA:
        red, green, blue, al = emoji_analyzer.get_average_color_text(e, show=False, background=(255, 255, 255, 255))
        if red == 255 and green == 255 and blue == 255:
            print('shitty')
            continue

        result.append([red, green, blue, e])

    with open('emojis.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4)

    print("DONE!")

