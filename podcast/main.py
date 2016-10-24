import argparse
import pprint
from collections import Counter

from cache import save_radio
from channel_config import load_channel_config
from download import download_channel
from models import Radio
from update import update_channel


def print_status(radio):
    pprint.pprint(dict(
        Counter(
            (channel.channel_info.name, type(podcast.status).__name__)
            for channel in radio.channels
            for podcast in channel.known_podcasts)))


def load_radio(directory, config):
    return Radio(
        channels=load_channel_config(directory, config),
        directory=directory)


def update_radio(radio):
    return [
        update_channel(channel)
        for channel in radio.channels
    ]


def download_radio(radio):
    return [
        download_channel(radio.directory, channel)
        for channel in radio.channels
    ]


def save(radio, directory):
    save_radio(radio, directory)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loads podcasts.')
    parser.add_argument('command')
    parser.add_argument('--config')
    parser.add_argument('--directory')
    args = parser.parse_args()

    radio = load_radio(args.config, args.directory)

    action = {
        'download': download_radio,
        'update': update_radio,
        'status': print_status,
    }

    maybe_radio = action[args.command](radio)

    if maybe_radio:
        save(maybe_radio, args.directory)
