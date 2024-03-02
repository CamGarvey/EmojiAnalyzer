import json

import requests

from src.emoji_analyzer import EmojiAnalyzer
from src.helpers.emoji_helper import render, codepoints, rgi
from src.helpers.math import map_number
from src.sources.text_base_source import TextBaseSource


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


def get_google_emoji_ordering(exclude_groups=None, include_alternate=True):
    emoji_ordering = requests.get(
        'https://cdn.jsdelivr.net/gh/googlefonts/emoji-metadata@main/emoji_15_1_ordering.json').json()

    groups = emoji_ordering if not exclude_groups else filter(lambda x: x['group'] not in exclude_groups,
                                                              emoji_ordering)
    for group in groups:
        print(group['group'])
        for emoji in group['emoji']:
            unicode = render(emoji['base'])
            yield unicode
            if include_alternate:
                for alternate in emoji['alternates']:
                    yield render(alternate)


def get_apple_emoji_ordering(exclude_groups=None, include_alternate=True):
    emoji_ordering = requests.get('https://cdn.jsdelivr.net/npm/emoji-datasource-apple@15.1.2/emoji.json').json()

    groups = []
    uniquekeys = []
    emoji_ordering = sorted(emoji_ordering, key=lambda x: x['category'])
    for k, g in groupby(emoji_ordering, lambda x: x['category']):
        groups.append(list(g))  # Store group iterator as a list
        uniquekeys.append(k)
    # groups = emoji_ordering if not exclude_groups else filter(lambda x: x not in exclude_groups, emoji_ordering)
    for index, group in enumerate(groups):
        print(uniquekeys[index])
        for emoji in group:
            unicode = render(emoji['google'])
            yield unicode
            if include_alternate:
                for alternate in emoji['alternates']:
                    yield render(alternate)


def get_average_color_of_emojis_generator(get_ordering_func, emoji_analyzer: EmojiAnalyzer, exclude_groups=None,
                                          background=None):
    """
    Uses google ordering so some emojis might be missing for apple
    """
    for unicode in get_ordering_func(exclude_groups):
        try:
            red, green, blue, alpha = emoji_analyzer.get_average_color(unicode, background=background)

            if (red <= background[0] and green <= background[1] and blue <= background[2]) or alpha == 0:
                print(f"{unicode} - Skipping; could not see it")
                continue

            alpha = round(map_number(alpha, 0, 255, 0, 1), 2)

            print(unicode, [red, green, blue, alpha])
            yield {
                'emoji': unicode,
                'rgb': [red, green, blue, alpha]
            }
        except Exception as e:
            print(e)
            print(f"{unicode} - Failed")


def get_average_color_of_emojis_generator2(emoji_analyzer: EmojiAnalyzer, background=None):
    import emoji

    for unicode in emoji.EMOJI_DATA:
        try:
            red, green, blue, alpha = emoji_analyzer.get_average_color(unicode, background=background)

            if (red <= background[0] and green <= background[1] and blue <= background[2]) or alpha == 0:
                print(f"{unicode} - Skipping; could not see it")
                continue

            alpha = round(map_number(alpha, 0, 255, 0, 1), 2)

            print(unicode, [red, green, blue, alpha])
            yield {
                'emoji': unicode,
                'rgb': [red, green, blue, alpha]
            }
        except Exception as e:
            print(e)
            print(f"{unicode} - Failed")


def create_apple_emoji_analyzer(font_size):
    font_path = '/System/Library/Fonts/Apple Color Emoji.ttc'
    return EmojiAnalyzer(font_path, font_size, source=TextBaseSource(font_path, font_size=font_size))


def create_noto_emoji_analyzer():
    font_size = 109  # only font size
    font_path = '/Users/camerongarvey/Documents/Repos/noto-emoji/fonts/NotoColorEmoji.ttf'
    source = TextBaseSource(font_path, font_size=font_size, padding=20)
    return EmojiAnalyzer(font_path, font_size, source=source)


apple_font = [20, 26, 32, 40, 48, 52, 64, 96, 160]


def get_apple_from_font(background):
    result = []
    font_size = 160
    font_path = '/System/Library/Fonts/Apple Color Emoji.ttc'

    emoji_analyzer = EmojiAnalyzer(font_path, font_size, source=TextBaseSource(font_path, font_size=font_size))
    emoji_ordering = requests.get(
        'https://cdn.jsdelivr.net/gh/googlefonts/emoji-metadata@main/emoji_15_1_ordering.json').json()

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
    bad = []
    for unicode in emoji.EMOJI_DATA:
        try:
            red, green, blue, alpha = emoji_analyzer.get_average_color(unicode, background=background)
        except:
            bad.append(unicode)
            continue
        if (red <= background[0] and green <= background[1] and blue <= background[2]) or alpha == 0:
            print('No emoji')
            bad.append(unicode)
            continue

        alpha = round(map_number(alpha, 0, 255, 0, 1), 2)
        print(f"{unicode} - [{red}, {green}, {blue}, {alpha}]")

        result.append({
            'emoji': unicode,
            'rgb': [red, green, blue, alpha]
        })

    print('bad', bad)

    return result


def export_noto_emojis(font_size: int, output_size: int):
    emoji_analyzer = create_noto_emoji_analyzer()
    for unicode in get_google_emoji_ordering():
        print('adding', unicode)
        try:
            emoji_analyzer.download_png(unicode, (0, 0, 0, 0), f'emojis/noto/{output_size}/{unicode}.png',
                                        output_size=(output_size, output_size))
        except Exception as error:
            print('failed', error)


def export_apple_emojis(font_size: int, output_size: int):
    import emoji
    font_path = '/System/Library/Fonts/Apple Color Emoji.ttc'
    emoji_analyzer = EmojiAnalyzer(font_path, font_size, source=TextBaseSource(font_path, font_size=font_size))

    for unicode in emoji.EMOJI_DATA:
        print('adding', unicode)
        try:
            emoji_analyzer.download_png(unicode, (0, 0, 0, 0), f'emojis/apple/{output_size}/{unicode}.png',
                                        output_size=(output_size, output_size))
        except:
            print('failed')


def find_font_sizes(font_path, show=False):
    sizes = []
    for i in range(1000):
        try:
            source = TextBaseSource(font_path, font_size=i)
            emoji_analyzer = EmojiAnalyzer(font_path, i, source=source)
            emoji_analyzer.get_average_color('👨‍🏫', background=(0, 0, 0, 255), show=show)
            sizes.append(i)
        except Exception as e:
            pass
    return sizes


if __name__ == '__main__':
    analyzer = create_apple_emoji_analyzer(160)
    # analyzer.get_average_color('', (0,0,0,0), show=True)

    results = list(get_average_color_of_emojis_generator(get_google_emoji_ordering, analyzer, background=(0, 0, 0, 0)))
    with open('emojis.json', "w", encoding="utf-8") as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)

    # print("DONE!")

# These are the apple emojis that pillow doesn't like
# {'google': 3827, 'appleEmoji': 4390}
