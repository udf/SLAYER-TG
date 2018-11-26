import xml.etree.ElementTree as ET
from common import *


INHIBITORS = [
    InhibitorHTML(),
    InhibitorPercentFormatter(),
    InhibitorUrl(),
    InhibitorUsernamePlaceholder()
]

IGNORED_KEYS = {
    'default_web_client_id',
    'firebase_database_url',
    'gcm_defaultSenderId',
    'google_api_key',
    'google_app_id',
    'google_crash_reporting_api_key',
    'google_storage_bucket',
    'project_id'
}


def unescape(string):
    return re.sub(r'\\(.)', r'\1', string)


def escape(string):
    return re.sub(r'(["\'])', r'\\\1', string)


def get_new_string(name, text):
    if name == 'LanguageCode':
        return 'en1'
    if name in ('chatDate', 'chatFullDate') or name.startswith('format'):
        return text

    return escape(FVCK_SHIT_UP(INHIBITORS, unescape(text)))


def generate_pack(path):
    tree = ET.parse(path)
    root = tree.getroot()
    chat_admin_string = None
    pending_remove = []
    for string in root:
        name = string.get('name')
        if name in IGNORED_KEYS:
            pending_remove.append(string)
            continue
        string.text = get_new_string(name, string.text)
        if name == 'ChatAdmin':
            chat_admin_string = string

    if chat_admin_string is None:
        raise RuntimeError('ChatAdmin string not found!')

    for key in pending_remove:
        root.remove(key)

    badges = ('🤘', '\u2063', '★')
    badge_names = ('EMOJI', 'NO', 'STAR')
    files = []
    for badge, badge_name in zip(badges, badge_names):
        chat_admin_string.text = badge
        files.append(f'ANDROID-{badge_name}-BADGE.xml')
        tree.write(files[-1])

    return files


if __name__ == '__main__':
    generate_pack('English.xml')
