import os
import pickle
import typing

from podcast.models import Channel
from podcast.models import ChannelInfo
from podcast.models import Podcast
from podcast.models import Radio
from podcast.models import RadioDirectory


CACHE_LOCATION = '.cache'


def _cache_location(
        directory: RadioDirectory,
        channel_info: ChannelInfo) -> str:
    return os.path.join(
        directory,
        channel_info.directory,
        CACHE_LOCATION)


def load_known_podcasts(
        directory: RadioDirectory,
        channel_info: ChannelInfo
) -> typing.List[Podcast]:
    filename = _cache_location(directory, channel_info)
    if not os.path.exists(filename):
        return []

    with open(filename, 'rb') as f:
        cache = pickle.load(f)

    return cache


def save_known_podcasts(
        directory: RadioDirectory,
        channel: Channel
) -> None:
    filename = _cache_location(directory, channel.channel_info)

    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    with open(filename, 'wb') as f:
        pickle.dump(channel.known_podcasts, f)


def save_radio(radio: Radio) -> None:
    for channel in radio.channels:
        save_known_podcasts(radio.directory, channel)
