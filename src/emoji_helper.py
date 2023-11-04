def codepoints(unicode):
    return [ord(char) for char in unicode]


def rgi(code_points):
    return '_'.join([format(code_point, '04x') for code_point in code_points])


def render(code_points):
    return ''.join([chr(code_point) for code_point in code_points])