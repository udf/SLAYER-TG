import xml.etree.ElementTree as ET
from common import *

def unescape(string):
    return re.sub(r'\\(.)', r'\1', string)

def escape(string):
    return re.sub(r'(["\'])', r'\\\1', string)

def get_new_string(name, text):
    if name == 'LanguageCode':
        return 'en1'
    if name in ['chatDate','chatFullDate'] or name.startswith('format'):
        return text

    return escape(FVCK_SHIT_UP(inhibitors, unescape(text)))


inhibitors = [
    InhibitorHTML(),
    InhibitorPercentFormatter(),
    InhibitorUrl(),
    InhibitorUsernamePlaceholder()
]

ignored_keys = {'default_web_client_id', 'firebase_database_url', 'gcm_defaultSenderId', 'google_api_key', 'google_app_id', 'google_crash_reporting_api_key', 'google_storage_bucket', 'project_id'}
pending_remove = []
tree = ET.parse('English.xml')

chat_admin_string = None
root = tree.getroot()
for string in root:
    name = string.get('name')
    if name in ignored_keys:
        pending_remove.append(string)
        continue

    string.text = get_new_string(name, string.text)
    if name == 'ChatAdmin':
        chat_admin_string = string

for key in pending_remove:
    root.remove(key)

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