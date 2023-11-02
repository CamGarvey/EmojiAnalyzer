import emoji
import json

from pilmoji.source import Twemoji

from emoji_analyzer import EmojiAnalyzer
from sources.file_base_source import FileBaseSource
from sources.text_base_source import TextBaseSource


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

    emoji_analyzer = EmojiAnalyzer(font_path, source=TextBaseSource(font_path, font_size=font_size))
    # emoji_analyzer = EmojiAnalyzer(font_path, source=FileBaseSource(noto_path_builder))
    # emoji_analyzer = EmojiAnalyzer(font_path)

    colors = emoji_analyzer.get_dominant_colors('👩‍🦯', show=True, font_size=font_size, background=(0, 0, 0, 255))

    red = 0
    green = 0
    blue = 0
    for (r, g, b) in colors:
        red += r
        green += g
        blue += b

    l = len(colors)
    c = (int(red / l), int(g / l), int(b / l))

    for e in emoji.EMOJI_DATA:
        print('')
        print(e)
        (red, green, blue) = emoji_analyzer.get_dominant_colors(e, font_size=font_size, background=(0, 0, 0, 0))
        print(red, green, blue)
        if red == 0 & green == 0 & blue == 0:
            print('shitty')
            continue

        # result.append({"r": red, "g": green, "b": blue, "a": round((1 / 255) * alpha, 2), 'emoji': e})
        result.append({
            "red": red,
            "green": green,
            "blue": blue,
            # "alpha": round((1 / 255) * alpha, 2),
            'emoji': e
        })

    with open('emojis.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4)

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
