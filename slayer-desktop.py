from common import *
import re
from ast import literal_eval
from collections import OrderedDict


def escape(string):
    return re.sub(r'(["\\])', r'\\\1', string).replace('\n', '\\n')


def get_new_string(key, text):
    if key == 'lng_language_name':
        return 'SLAYER'

    return FVCK_SHIT_UP(inhibitors, text)


def parse_strings(filepath):
    """Quick and dirty (and likely broken) parser for telegram desktop .strings files"""
    def get_debug_info():
        """Returns the line and column that offset is at"""
        line_start = data.rfind('\n', 0, offset)
        if line_start == -1:
            line = 1
        else:
            line = data.count('\n', 0, line_start + 1) + 1
        return f'line {line}, col {offset - line_start}'

    data = ''

    with open(filepath) as file:
        data = file.read()

    stack = []
    offset = 0
    strings = OrderedDict()
    while offset < len(data):
        peak = data[offset:offset+2]
        if data[offset].isspace():
            offset += 1
            continue

        # skip block comments
        if peak.startswith('/*'):
            end = data.find('*/', offset)
            if end == -1:
                raise RuntimeError(f'Unterminated block comment at {get_debug_info()}')
            offset += end + 2
            continue

        # ignore line comments
        if peak.startswith('//'):
            offset = data.find('\n', offset) + 1
            if offset == 0:
                break
            continue

        if data[offset] == '=':
            # TODO probably store the operator or something
            # probably not needed because there is only one operator in .strings
            offset += 1
            continue

        # if we see a quote, grab the rest of the string and throw it on the stack
        if data[offset] == '"':
            match = re.match(r'".+?[^\\]"', data[offset:])
            stack.append(literal_eval(match.group(0)))
            offset += match.end()
            continue

        # if we see a terminating token, then add the last two strings from the stack to 
        # our output, usually we would want to do something with the stored operator here
        # but there is only one operator in .strings, so ¯\_(ツ)_/¯
        if data[offset] == ';':
            if len(stack) <= 0:
                offset += 1
                continue
            if len(stack) < 2:
                print(f'WARNING: Ignoring string "{stack[0]}" (before {get_debug_info()})')
                offset += 1
                stack.clear()
                continue
            if len(stack) > 2:
                print(f'WARNING: Ignoring extra string(s) "{stack[:-2]}" (before {get_debug_info()})')

            strings[stack[-2]] = stack[-1]
            stack.clear()
            offset += 1
            continue

        raise RuntimeError(f'Unrecognised token "{data[offset]}" at {get_debug_info()}')

    return strings


def write_strings(strings, filename):
    """Writes strings dictionary to .strings file"""
    with open(filename, 'w') as file:
        for key, string in strings.items():
            file.write(
                '"{}" = "{}";\n'.format(
                    key,
                    escape(string),
                )
            )


inhibitors = [
    InhibitorDesktopFormatter(),
    InhibitorMarkdownTag(),
]

try:
    strings = parse_strings('English.strings')
except RuntimeError as e:
    print('Failed to parse .strings file:', e)
    exit(1)


for key, string in strings.items():
    strings[key] = get_new_string(key, string)

# \m/ emoji
strings['lng_admin_badge'] = '🤘'
write_strings(strings, 'SLAYER-EMOJI.strings')

# blank
strings['lng_admin_badge'] = ''
write_strings(strings, 'SLAYER-no.strings')

# star
strings['lng_admin_badge'] = '★'
write_strings(strings, 'SLAYER-star.strings')
