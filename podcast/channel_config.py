import yaml

from models import Channel
from models import ChannelInfo
from cache import load_known_podcasts


def parse_channel_info(channel_dict):
    return ChannelInfo(
        name=channel_dict['name'],
        url=channel_dict['url'],
        directory=channel_dict['directory'])


def load_channel(directory, channel_config):
    channel_info = parse_channel_info(channel_config)

    return Channel(
        channel_info=channel_info,
        known_podcasts=load_known_podcasts(directory, channel_info))


def load_channel_config(directory, filename):
    with open(filename) as f:
        radio_config = yaml.load(f)

    return [load_channel(directory, channel_config)
            for channel_config in radio_config]
