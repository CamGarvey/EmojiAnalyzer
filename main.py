import emoji
import json
from emoji_analyzer import EmojiAnalyzer

if __name__ == '__main__':
    # Example usage:
    result = []

    emoji_analyzer = EmojiAnalyzer('/System/Library/Fonts/Apple Color Emoji.ttc')

    # print(emoji_to_average_color('🎾')) # transparent
    # print(emoji_to_average_color('🎾', background=(0, 0, 0, 255))) # black background
    # print(emoji_to_average_color('🎾', background=(255, 255, 255, 255))) # white background

    for e in emoji.EMOJI_DATA:
        red, green, blue, al = emoji_analyzer.get_average_color(e, background=(0, 0, 0, 255))
        if red != 0 and green != 0 and blue != 0:
            result.append([red, green, blue, e])

    with open('emojis.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

