import argparse
import pprint
import typing  # noqa
from collections import Counter

from podcast.cache import save_radio
from podcast.channel_config import load_channel_config
from podcast.download import download_channel
from podcast.models import Radio
from podcast.models import RadioDirectory
from podcast.update import update_channel


def print_status(radio: Radio) -> Radio:
    pprint.pprint(dict(
        Counter(
            (channel.channel_info.name, type(podcast.status).__name__)
            for channel in radio.channels
            for podcast in channel.known_podcasts)))

    return radio


def load_radio(directory: RadioDirectory, config: str) -> Radio:
    return Radio(
        channels=load_channel_config(directory, config),
        directory=RadioDirectory(directory))


def update_radio(radio: Radio) -> Radio:
    updated_channels = [
        update_channel(channel)
        for channel in radio.channels
    ]

    return radio._replace(channels=updated_channels)


def download_radio(radio: Radio) -> Radio:
    downloaded_channels = [
        download_channel(radio.directory, channel)
        for channel in radio.channels
    ]

    return radio._replace(channels=downloaded_channels)


def save(radio: Radio) -> None:
    save_radio(radio)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loads podcasts.')
    parser.add_argument('command')
    parser.add_argument('--config')
    parser.add_argument('--directory')
    args = parser.parse_args()

    print("Loading radio...")

    radio = load_radio(args.directory, args.config)

    action = {
        'status': print_status,
        'update': update_radio,
        'download': download_radio,
    }  # type: typing.Dict[str, typing.Callable[[Radio], Radio]]

    radio = action[args.command](radio)

    print("Saving radio...")
    save(radio)

    print("Done. Goodbye.")
