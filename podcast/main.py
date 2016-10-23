import argparse
from collections import Counter
import pprint

from cache import save_radio
from channel_config import load_channel_config
from update import update_channel
from download import download_channel

def print_status(radio):
    pprint.pprint(dict(
            Counter(
                (channel.channel_info.name, type(podcast).__name__)
                for channel in radio
                for podcast in channel.known_podcasts)))

def load_radio(directory, config):
    load_channel_config(directory, config)

def update_radio(radio):
    return [
        update_channel(channel)
        for channel in radio
    ]

def download_radio(directory, config):
    return [
        download_channel(channel)
        for channel in radio
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