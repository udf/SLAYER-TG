# Pulls language files from Github and builds both versions of the pack
# and uploads them to a channel using Telethon
import os
import asyncio
import hashlib
import logging
import urllib.request
from configparser import ConfigParser, DuplicateSectionError

from telethon import TelegramClient

import slayer_android
import slayer_desktop


class Pack:
    """respresents a language pack to be built"""
    def __init__(self, name, url, build_func):
        self.name = name
        self.url = url
        self.build_func = build_func


def md5_file(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


PACKS = (
    Pack(
        name='Telegram Desktop',
        url='https://raw.githubusercontent.com/telegramdesktop/tdesktop/master/Telegram/Resources/langs/lang.strings',
        build_func=slayer_desktop.generate_pack
    ),
    Pack(
        name='Telegram Android',
        url='https://raw.githubusercontent.com/DrKLO/Telegram/master/TMessagesProj/src/main/res/values/strings.xml',
        build_func=slayer_android.generate_pack
    ),
)

CHANNEL_HANDLE = '@SLAYERPACK'
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

client = TelegramClient("bot", 6, "eb06d4abfb49dc3eeb1aeb98ae0f581e")

checksums = ConfigParser()
checksums.read('build.ini')
try:
    checksums.add_section('checksums')
except DuplicateSectionError:
    pass


# Build packs, if their sources differ from what we used last time
files_to_upload = []
for pack in PACKS:
    logger.info(f'Downloading pack for {pack.name}...')
    path, response = urllib.request.urlretrieve(pack.url)

    checksum = md5_file(path)
    if checksums.get('checksums', pack.name, fallback='') == checksum:
        logger.info(f"Skipping build because checksum hasn't changed")
        continue
    checksums.set('checksums', pack.name, checksum)

    logger.info(f'Building {pack.name} from {path}...')
    files_to_upload.extend(pack.build_func(path))

if not files_to_upload:
    logger.info('There is nothing to do.')
    exit()


async def upload_to_channel():
    await client.start(bot_token=os.environ['TOKEN'])
    for file in files_to_upload:
        await client.send_file(CHANNEL_HANDLE, file)

logger.info(f'Uploading files...')
asyncio.get_event_loop().run_until_complete(upload_to_channel())

with open('build.ini', 'w') as f:
    checksums.write(f)
