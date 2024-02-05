from typing import Union, Type, Tuple

from PIL import Image, ImageFont
import numpy as np
from pilmoji import Pilmoji
from pilmoji.source import BaseSource, AppleEmojiSource
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

from src.helpers.math import map_number


class EmojiAnalyzer:

    def __init__(self, font_path, font_size, source: Union[BaseSource, Type[BaseSource]] = AppleEmojiSource):
        self.font_path = font_path
        self.font_size = font_size
        self.source = source

    def get_average_color(self, emoji: str, background: (int, int, int, int), show=False) -> Tuple[int, int, int, int]:
        with Image.new(mode='RGBA', size=(self.font_size, self.font_size), color=background) as image:
            font = ImageFont.truetype(self.font_path, self.font_size)

            with Pilmoji(image, source=self.source) as pilmoji:
                pilmoji.text((0, 0), emoji, (0, 0, 0), font)

            rgba_color = self.extract_average_color(image, background)
            if show:
                fig, ax = plt.subplots()
                # Create a single pixel with the specified color
                ax.imshow([[rgba_color]])
                # Remove axis labels and ticks for a cleaner look
                ax.set_xticks([])
                ax.set_yticks([])
                image.show()
                plt.show()

            return rgba_color

    def get_dominant_colors(self, emoji: str, background: (int, int, int, int), n_colors=4, show=False):
        with Image.new(mode='RGBA', size=(self.font_size, self.font_size), color=background) as image:
            font = ImageFont.truetype(self.font_path, self.font_size)

            with Pilmoji(image, source=self.source) as pilmoji:
                pilmoji.text((0, 0), emoji, (0, 0, 0), font)

            if show:
                image.show()

            return self.extract_dominant_colors(image, n_colors, show)

    def extract_dominant_colors2(self, image, colors, show=False):
        # Convert the image to the CIELAB color space
        image_lab = image.convert('LAB')

        # Convert the CIELAB image to a NumPy array
        image_array = np.array(image_lab)

        # Reshape the array to a 2D array of pixels (rows) by LAB values (columns)
        pixels = image_array.reshape((-1, 3))

        # Use K-means clustering to find dominant colors
        kmeans = KMeans(n_clusters=colors, random_state=0).fit(pixels)

        # Get the cluster centers, which represent the dominant colors in LAB color space
        dominant_colors_lab = kmeans.cluster_centers_

        return dominant_colors_lab

    def extract_dominant_colors(self, image: Image, colors, show=False):
        # Set the desired number of colors for the image
        img = image.quantize(colors=colors, kmeans=colors).convert('RGB')

        dom_colors = sorted(img.getcolors(2 ** 24), reverse=True)[:colors]
        values = [item[0] for item in dom_colors]
        colors = [item[1] for item in dom_colors]
        if show:
            # Create a bar chart with the numeric values
            plt.bar(range(len(values)), values, color=[(r / 255, g / 255, b / 255) for (r, g, b) in colors])
            plt.xticks(range(len(values)), [str(item) for item in values])

            plt.xlabel('Index')
            plt.ylabel('Occurrences')
            plt.title('Colour')
            plt.show()

        return colors

    def extract_dominant_color2(self, image):
        try:
            reduced = image.convert("P", palette=Image.WEB)  # convert to web palette (216 colors)
            palette = reduced.getpalette()  # get palette as [r,g,b,r,g,b,...]
            palette = [palette[3 * n:3 * n + 3] for n in range(256)]  # group 3 by 3 = [[r,g,b],[r,g,b],...]
            color_count = [(n, palette[m]) for n, m in reduced.getcolors()]
            return color_count[0]
        except Exception as e:
            print("Failed to find dominant color")
            raise e

    def extract_average_color(self, image: Image, background) -> Tuple[int, int, int, int]:
        try:
            image_array = np.array(image)
            if len(background) == 3 or background[3] != 0:
                # Calculate the average color by taking the mean of all pixel values
                # average_color = np.mean(image_array, axis=(0, 1))
                average_color = image_array.mean(axis=0).mean(axis=0)
                return tuple(map(int, average_color))

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

    def download_png(self, emoji: str, background, path, show=False, output_size=None):

        with Image.new(mode='RGBA', size=(self.font_size, self.font_size), color=background) as image:
            font = ImageFont.truetype(self.font_path, self.font_size)

            with Pilmoji(image, source=self.source) as pilmoji:
                pilmoji.text((0, 0), emoji, (0, 0, 0), font)

            if show:
                image.show()

            if output_size:
                image = image.resize(output_size, Image.LANCZOS)

            if show:
                image.show()

            image.save(path)
