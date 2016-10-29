import typing
from collections import Counter

from podcast.info import InfoContent
from podcast.models import get_channel_id
from podcast.models import Radio


def print_status(radio: Radio) -> typing.Tuple[Radio, InfoContent]:
    status = InfoContent(dict(Counter(
        '{0} -- {1}'.format(
            get_channel_id(channel),
            type(podcast.status).__name__)
        for channel in radio.channels
        for podcast in channel.known_podcasts)))

    return radio, status


def has_new_podcast_from_channel(
        radio: Radio,
        channel_id: str
) -> typing.Tuple[Radio, InfoContent]:
    info_content = {'has_new': False}
    for channel in radio.channels:
        if get_channel_id(channel) == channel_id:
            for podcast in channel.known_podcasts:
                if type(podcast.status).__name__ == 'NewStatus':
                    info_content['has_new'] = True
                    break
    return radio, InfoContent(info_content)
