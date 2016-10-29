import typing

import jsonschema
import yaml

from podcast.cache import load_known_podcasts
from podcast.models import Channel
from podcast.models import ChannelInfo
from podcast.models import get_channel_id
from podcast.models import Radio
from podcast.models import RadioDirectory

schema = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["name", "url", "directory"],
        "properties": {
            "name": {"type": "string"},
            "url": {"type": "string"},
            "directory": {"type": "string"},
        }
    }
}


def _validate_config(config: typing.Any) -> None:
    jsonschema.validate(config, schema)


def _validate_channels(channels: typing.List[Channel]) -> None:
    channel_ids = [get_channel_id(channel) for channel in channels]

    has_no_duplicates = len(channel_ids) == len(set(channel_ids))

    assert has_no_duplicates, "channel directories aren't unique"


def parse_channel_info(channel_dict: dict) -> ChannelInfo:
    return ChannelInfo(
        name=channel_dict['name'],
        url=channel_dict['url'],
        directory=channel_dict['directory'])


def load_channel(
        directory: RadioDirectory,
        channel_config: dict) -> Channel:
    channel_info = parse_channel_info(channel_config)

    return Channel(
        channel_info=channel_info,
        known_podcasts=load_known_podcasts(directory, channel_info))


def load_channel_config(
        directory: RadioDirectory,
        filename: str) -> typing.List[Channel]:
    with open(filename) as f:
        radio_config = yaml.load(f)
        _validate_config(radio_config)

    channels = [load_channel(directory, channel_config)
                for channel_config in radio_config]
    _validate_channels(channels)
    return channels


def load_radio(
        directory: RadioDirectory,
        config: str
) -> Radio:

    return Radio(
        channels=load_channel_config(directory, config),
        directory=RadioDirectory(directory))
