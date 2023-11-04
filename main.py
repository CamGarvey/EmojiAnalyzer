import json

import requests

from src.emoji_analyzer import EmojiAnalyzer
from src.emoji_helper import render, codepoints, rgi
from src.sources.file_base_source import FileBaseSource
from src.sources.noto_color_emoji_source import NotoColorEmojiSource
from src.sources.text_base_source import TextBaseSource


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


def noto_path_builder2(emoji: str):
    return f"assets/128/emoji_u{rgi(codepoints(emoji))}.png"


def get_noto_from_ttf(background):
    result = []
    font_size = 109
    font_path = '/Users/camerongarvey/Documents/Repos/pixeled/public/NotoColorEmoji.ttf'

    emoji_analyzer = EmojiAnalyzer(font_path, font_size, source=TextBaseSource(font_path, font_size=font_size, padding=15))
    emoji_ordering = requests.get(
        'https://cdn.jsdelivr.net/gh/googlefonts/emoji-metadata@main/emoji_15_0_ordering.json').json()

    for group in emoji_ordering:
        print(group['group'])
        for emoji in group['emoji']:
            unicode = render(emoji['base'])
            red, green, blue, _ = emoji_analyzer.get_average_color(unicode, background=background)

            print(f"{unicode} - {' '.join(emoji['shortcodes'])} - [{red}, {green}, {blue}]")

            result.append({
                'emoji': unicode,
                'rgb': [red, green, blue]
            })

    return result


apple_font = [20, 26, 32, 40, 48, 52, 64, 96, 160]

if __name__ == '__main__':
    result = get_noto_from_ttf((0, 0, 0, 255))

    with open('emojis.json', "w", encoding="utf-8") as json_file:
        json.dump(result, json_file, ensure_ascii=True, indent=4)

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
