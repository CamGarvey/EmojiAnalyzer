import emoji
import json

from pilmoji.source import Twemoji

from emoji_analyzer import EmojiAnalyzer
from sources.file_base_source import FileBaseSource
from sources.text_base_source import TextBaseSource
import matplotlib.pyplot as plt

def map_number(input: int, input_min: int, input_max: int, output_min: int, output_max: int):
    return output_min + ((output_max - output_min) / (input_max - input_min)) * (input - input_min);


def get_color(dominant_colors):
    # Initialize weighted sums for each channel
    weighted_red, weighted_green, weighted_blue = 0, 0, 0

    # Define weights for each color (you can adjust these as needed)
    weights = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]  # Weights for the first, second, and third colors

    for i, (r, g, b) in enumerate(dominant_colors):
        # Apply weights to the colors
        weighted_red += r * weights[i]
        weighted_green += g * weights[i]
        weighted_blue += b * weights[i]

    # Normalize the weighted sums
    max_weight = sum(weights)
    red = int(weighted_red / max_weight)
    green = int(weighted_green / max_weight)
    blue = int(weighted_blue / max_weight)

    # Ensure the values are within the RGB range [0, 255]
    red = max(0, min(255, red))
    green = max(0, min(255, green))
    blue = max(0, min(255, blue))

    return red, green, blue


def noto_path_builder(emoji: str):
    path = f"assets/128/"
    prefix = "emoji_u"
    extension = ".png"

    codes = []
    for c in emoji:
        code = f'{ord(c):X}'
        if code == 'FE0F':
            break
        codes.append(code)

    return f"{path}{prefix}{'_'.join(codes)}{extension}".lower()


apple_font = [20, 26, 32, 40, 48, 52, 64, 96, 160]

if __name__ == '__main__':
    result = []

    font_size = 109  # noto
    # font_size = 64  # apple

    # font_path = '/System/Library/Fonts/Apple Color Emoji.ttc'
    font_path = '/Users/camerongarvey/Downloads/NotoColorEmoji.ttf'

    emoji_analyzer = EmojiAnalyzer(font_path, font_size, source=TextBaseSource(font_path, font_size=font_size))


    # color = emoji_analyzer.get_average_color('🙆🏻‍♂', background=(0, 0, 0, 255), show=True)

    for e in emoji.EMOJI_DATA:
        print('')
        print(e)
        red, green, blue, _ = emoji_analyzer.get_average_color(e, background=(0, 0, 0, 255))

        if red == 0 & green == 0 & blue == 0:
            print('shitty')
            continue

        result.append({
            'emoji': e,
            'rgb': [red, green, blue]
        })

    with open('emojis.json', "w", encoding="utf-8") as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)

    print("DONE!")





def find_font_sizes(emoji_analyzer, show=False):
    sizes = []
    for i in range(1000):
        try:
            emoji_analyzer.get_average_color_rgba('👨‍🏫', font_size=i, background=(0, 0, 0, 255), show=show)
            sizes.append(i)
        except:
            pass
    return sizes;
