import xml.etree.ElementTree as ET
from common import *

def unescape(string):
    return multi_sub(string, [
                        (r'\\n', r'\n'),
                        (r'\\(.)', r'\1')
                    ])
def escape(string):
    return multi_sub(string, [
                        (r'\n', r'\\n'),
                        (r'(["\'])', r'\\\1')
                    ])

def get_new_string(name, text):
    if name == 'LanguageCode':
        return 'en1'
    if name in ['chatDate','chatFullDate'] or name.startswith('format'):
        return text

    return escape(FVCK_SHIT_UP(inhibitors, unescape(text)))


inhibitors = [
    Inhibitor_HTML(),
    Inhibitor_percent_formatter(),
    Inhibitor_url(),
    Inhibitor_username_placeholder()
]

tree = ET.parse('English.xml')

chat_admin_string = None
for string in tree.getroot():
    name = string.attrib['name']
    string.text = get_new_string(name, string.text)
    if name == 'ChatAdmin':
        chat_admin_string = string


if chat_admin_string is not None:
    # \m/ emoji
    chat_admin_string.text = '🤘'
    tree.write('SLAYER-EMOJI.xml')

    # invisible separator
    chat_admin_string.text = '⁣'
    tree.write('SLAYER-no.xml')

    # star
    chat_admin_string.text = '★'
    tree.write('SLAYER-star.xml')
else:
    tree.write('SLAYER.xml')