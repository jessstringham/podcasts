import typing
from collections import Counter

from podcast.files import download_location
from podcast.info import build_info_content
from podcast.info import InfoContent
from podcast.models import get_channel_id
from podcast.models import get_podcast_id
from podcast.models import Radio
from podcast.models import read_channel_from_id


def print_status(radio: Radio) -> typing.Tuple[Radio, InfoContent]:
    status = build_info_content(
        result=dict(Counter(
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

    info_content = build_info_content(result=False)

    channel = read_channel_from_id(radio, channel_id)
    for podcast in channel.known_podcasts:
        if type(podcast.status).__name__ == 'NewStatus':
            info_content = build_info_content(result=True)
            break
    return radio, info_content


def recent_podcast_from_channel(
        radio: Radio,
        channel_id: str,
) -> typing.Tuple[Radio, InfoContent]:

    info_content = build_info_content(error='none found')
    channel = read_channel_from_id(radio, channel_id)

    new_podcasts = filter(
        lambda podcast: type(podcast.status).__name__ == 'NewStatus',
        channel.known_podcasts)

    if new_podcasts:
        recent_podcast = sorted(
            new_podcasts,
            key=lambda p: p.data.published,
            reverse=True)[0]

        info_content = build_info_content(
            result={
                'path': download_location(
                    radio.directory,
                    channel,
                    recent_podcast),
                'channel_id': channel_id,
                'podcast_id': get_podcast_id(recent_podcast),
            })

    return radio, info_content
