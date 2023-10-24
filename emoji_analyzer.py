import math
from typing import Union, Type

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pilmoji import Pilmoji
from pilmoji.source import BaseSource, AppleEmojiSource


class EmojiAnalyzer:

    def __init__(self, font_path, source: Union[BaseSource, Type[BaseSource]] = AppleEmojiSource):
        self.font_path = font_path
        self.source = source

    def get_average_color(self, emoji: str, font_size=48, background: (int, int, int, int) = None, show=False):
        with Image.new('RGBA', (font_size, font_size), (0, 0, 0, 255) if not background else background) as image:
            font = ImageFont.truetype(self.font_path, font_size)

            with Pilmoji(image, source=self.source) as pilmoji:
                pilmoji.text((0, 0), emoji, (0, 0, 0), font)

            # Convert the image to a NumPy array for easier manipulation
            image_array = np.array(image)

            if show:
                image.show()

            if background and background[3] != 0:
                # Calculate the average color by taking the mean of all pixel values
                average_color = np.mean(image_array, axis=(0, 1))
            else:
                # Extract non-transparent pixels
                non_transparent_pixels = image_array[:, :, :-1][image_array[:, :, 3] > 0]

                # Calculate the average color by taking the mean of non-transparent pixel values
                if non_transparent_pixels.size > 0:
                    average_color = np.mean(non_transparent_pixels, axis=0)
                else:
                    # If there are no non-transparent pixels, return transparent black
                    average_color = (0, 0, 0)

            # Convert the average color to RGB format
            average_color = tuple(map(int, average_color))

            return average_color

    def get_average_color_rgba(self, emoji: str, padding=0, font_size=48, background: (int, int, int, int) = None, show=False):
        try:
            container_size = font_size + padding
            # Create a new image with a transparent background or background
            image = Image.new(mode="RGBA", size=(container_size, container_size),
                              color=(0, 0, 0, 0) if not background else background)
            draw = ImageDraw.Draw(image)

            # Use a large font size to draw the emoji in the center of the image
            font = ImageFont.truetype(self.font_path, font_size, encoding='unic')
            bbox = draw.textbbox((font_size, font_size), emoji, font=font)
            text_height = bbox[3] - bbox[1]
            text_width = bbox[2] - bbox[0]
            x = (container_size - text_width) / 2
            y = (container_size - text_height) / 2

            # Draw the emoji on the image
            draw.text((x, y), emoji, embedded_color=True, font=font)

            if show:
                image.show()
            # Convert the image to a NumPy array for easier manipulation
            image_array = np.array(image)

            if background and background[3] != 0:
                # Calculate the average color by taking the mean of all pixel values
                average_color = np.mean(image_array, axis=(0, 1))
                average_color = tuple(map(int, average_color))
                return average_color

            rgb_pixels = image_array[:, :, :-1][image_array[:, :, 3] > 0]

            # Calculate the average color by taking the mean of RGB channels
            average_rgb = np.mean(rgb_pixels, axis=0)

            if np.isnan(average_rgb).any():
                return 0, 0, 0, 0

            # Calculate the mean of the alpha channel separately
            average_alpha = np.mean(image_array[:, :, 3][image_array[:, :, 3] >= 0])

            average_rgba = (*average_rgb, int(average_alpha))

            # Convert the average color to RGBA format
            average_rgba = tuple(map(int, average_rgba))

            return average_rgba
        except Exception as e:
            print("Failed to find average color")
            raise e
