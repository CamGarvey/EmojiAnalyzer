import emoji
import json
from emoji_analyzer import EmojiAnalyzer

if __name__ == '__main__':
    # Example usage:
    result = []

    emoji_analyzer = EmojiAnalyzer('/System/Library/Fonts/seguiemj.ttf')
    # emoji_analyzer = EmojiAnalyzer('/System/Library/Fonts/Apple Color Emoji.ttc')

    for e in emoji.EMOJI_DATA:
        red, green, blue, al = emoji_analyzer.get_average_color(e, background=(0, 0, 0, 255))
        if red + green + blue > 100:
            result.append([red, green, blue, e])

    with open('emojis.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=True, indent=4)

