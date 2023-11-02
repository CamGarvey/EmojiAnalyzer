from io import BytesIO
from typing import Optional

from PIL import Image, ImageDraw, ImageFont
from pilmoji.source import BaseSource


class TextBaseSource(BaseSource):

    def __init__(self, font_path, font_size, padding=0):
        self.font_path = font_path
        self.font_size = font_size
        self.padding = padding

    def get_emoji(self, emoji: str, /) -> Optional[BytesIO]:
        """Retrieves a :class:`io.BytesIO` stream for the image of the given emoji."""
        container_size = self.font_size + self.padding

        # Create a new image with a transparent background or background
        with Image.new(mode='RGBA', size=(container_size, container_size), color=(0, 0, 0, 0)) as image:
            draw = ImageDraw.Draw(image)
            # Use a large font size to draw the emoji in the center of the image
            font = ImageFont.truetype(self.font_path, self.font_size, encoding='unic')
            bbox = draw.textbbox((self.font_size, self.font_size), emoji, font=font)
            text_height = bbox[3] - bbox[1]
            text_width = bbox[2] - bbox[0]
            x = (container_size - text_width) / 2
            y = (container_size - text_height) / 2

            # Draw the emoji on the image
            draw.text((x, y), emoji, embedded_color=True, font=font)

            bytes_io = BytesIO()
            image.save(bytes_io, format='PNG')

            return bytes_io;


    def get_discord_emoji(self, id: int, /) -> Optional[BytesIO]:
        raise NotImplementedError