from PIL import Image, ImageDraw, ImageFont
import numpy as np


class EmojiAnalyzer:

    def __init__(self, emoji_font_path):
        self.emoji_font_path = emoji_font_path

    def get_average_color(self, emoji: str, size=48, background: (int, int, int, int) = None):
        try:
            # Create a new image with a transparent background or background
            image = Image.new("RGBA", (size, size), (0, 0, 0, 0) if not background else background)
            draw = ImageDraw.Draw(image)

            # Use a large font size to draw the emoji in the center of the image
            font = ImageFont.truetype(self.emoji_font_path, size, encoding='unic')
            # font = ImageFont.truetype('/Users/camerongarvey/Downloads/AppleColorEmoji.ttf', size, encoding='unic')
            text_length = draw.textlength(emoji, font)
            x = (size - text_length) / 2

            # Draw the emoji on the image
            draw.text((x, x), emoji, embedded_color=True, font=font)

            # Convert the image to a NumPy array for easier manipulation
            image_array = np.array(image)

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
        except Exception as e:
            print("Failed to find average color")
            raise e
