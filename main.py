import json

import requests

from src.emoji_analyzer import EmojiAnalyzer
from src.helpers.emoji_helper import render, codepoints, rgi
from src.helpers.math import map_number
from src.sources.text_base_source import TextBaseSource



def get_average_color_from_domiant_colors(dominant_colors):
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


def get_noto_ordering(group_filter=None):
    emoji_ordering = requests.get(
        'https://cdn.jsdelivr.net/gh/googlefonts/emoji-metadata@main/emoji_15_0_ordering.json').json()

    groups = emoji_ordering if not group_filter else filter(lambda x: x['group'] in group_filter, emoji_ordering)
    for group in groups:
        print(group['group'])
        for emoji in group['emoji']:
            unicode = render(emoji['base'])
            yield unicode



def get_dominant_colors_noto(background, show=False, group_filter=None):
    result = []
    font_size = 109
    font_path = '/Users/camerongarvey/Documents/Repos/noto-emoji/fonts/NotoColorEmoji.ttf'

    emoji_analyzer = EmojiAnalyzer(font_path, font_size, source=TextBaseSource(font_path, font_size=font_size, padding=10))
    emoji_ordering = requests.get(
        'https://cdn.jsdelivr.net/gh/googlefonts/emoji-metadata@main/emoji_15_0_ordering.json').json()

    groups = group_filter if not group_filter else filter(lambda x: x['group'] in group_filter, emoji_ordering)
    for group in groups:
        print(group['group'])
        for emoji in group['emoji']:
            unicode = render(emoji['base'])
            # red, green, blue, alpha = emoji_analyzer.get_average_color(unicode, background=background, show=show)
            dominant_colors = emoji_analyzer.get_dominant_colors(unicode, background=background, show=show)
            red, green, blue, alpha = get_average_color_from_domiant_colors(dominant_colors)

            alpha = round(map_number(alpha, 0, 255, 0, 1), 2)
            print(f"{unicode} - {' '.join(emoji['shortcodes'])} - [{red}, {green}, {blue} {alpha}]")

            result.append({
                'emoji': unicode,
                'rgb': [red, green, blue, alpha]
            })

    return result


apple_font = [20, 26, 32, 40, 48, 52, 64, 96, 160]


def get_apple_from_font(background):
    result = []
    font_size = 160
    font_path = '/System/Library/Fonts/Apple Color Emoji.ttc'

    emoji_analyzer = EmojiAnalyzer(font_path, font_size, source=TextBaseSource(font_path, font_size=font_size))
    emoji_ordering = requests.get(
        'https://cdn.jsdelivr.net/gh/googlefonts/emoji-metadata@main/emoji_15_0_ordering.json').json()

    for group in emoji_ordering:
        print(group['group'])
        for emoji in group['emoji']:
            unicode = render(emoji['base'])
            red, green, blue, alpha = emoji_analyzer.get_average_color(unicode, background=background)

            if red == 0 and green == 0 and blue == 0:
                print('No emoji')
                continue

            print(f"{unicode} - {' '.join(emoji['shortcodes'])} - [{red}, {green}, {blue}, {alpha}]")

            alpha = round(map_number(alpha, 0, 255, 0, 1), 2)
            result.append({
                'emoji': unicode,
                'rgb': [red, green, blue, alpha]
            })

    return result


def get_apple_from_font_2(background):
    import emoji
    result = []
    font_size = 20
    font_path = '/System/Library/Fonts/Apple Color Emoji.ttc'

    emoji_analyzer = EmojiAnalyzer(font_path, font_size, source=TextBaseSource(font_path, font_size=font_size))
    bad = 0
    for unicode in emoji.EMOJI_DATA:
        try:
            red, green, blue, alpha = emoji_analyzer.get_average_color(unicode, background=background)
        except:
            bad += 1
            continue
        if (red <= background[0] and green <= background[1] and blue <= background[2]) or alpha == 0:
            print('No emoji')
            bad += 1
            continue

        alpha = round(map_number(alpha, 0, 255, 0, 1), 2)
        print(f"{unicode} - [{red}, {green}, {blue}, {alpha}]")

        result.append({
            'emoji': unicode,
            'rgb': [red, green, blue, alpha]
        })

    print('bad', bad)

    return result


def export_noto_emojis(font_size, output_size):
    import emoji
    font_path = '/Users/camerongarvey/Documents/Repos/noto-emoji/fonts/NotoColorEmoji.ttf'
    emoji_analyzer = EmojiAnalyzer(font_path, font_size,
                                   source=TextBaseSource(font_path, font_size=font_size, padding=10))
    for unicode in get_noto_ordering():
        print('adding', unicode)
        try:
            emoji_analyzer.download_png(unicode, (0, 0, 0, 0), f'emojis/noto/{output_size}/{unicode}.webp',
                                        output_size=(output_size, output_size))
        except Exception as error:
            print('failed', error)


def export_apple_emojis(font_size, output_size):
    import emoji
    font_path = '/System/Library/Fonts/Apple Color Emoji.ttc'
    emoji_analyzer = EmojiAnalyzer(font_path, font_size, source=TextBaseSource(font_path, font_size=font_size))

    for unicode in emoji.EMOJI_DATA:
        print('adding', unicode)
        try:
            emoji_analyzer.download_png(unicode, (0, 0, 0, 0), f'emojis/{output_size}/{unicode}.webp',
                                        output_size=(output_size, output_size))
        except:
            print('failed')


def find_font_sizes(emoji_analyzer, show=False):
    sizes = []
    for i in range(1000):
        try:
            emoji_analyzer.get_average_color('👨‍🏫', font_size=i, background=(0, 0, 0, 255), show=show)
            sizes.append(i)
        except Exception as e:
            print(e)
            pass
    return sizes


if __name__ == '__main__':
    # export_apple_emojis(160, 128)
    font_size = 109
    output_size = 128
    export_noto_emojis(font_size, font_size)
    # result = get_noto_from_ttf((0, 0, 0, 0), show=True, group_filter=['Flags'])
    # result = get_apple_from_font_2((0, 0, 0, 0))
    #
    # print(len(result))
    #
    # with open('emojis.json', "w", encoding="utf-8") as json_file:
    #     json.dump(result, json_file, ensure_ascii=False, indent=4)
    #
    # print("DONE!")
