import typing
from collections import Counter

from podcast.files import download_location
from podcast.info import build_info_content
from podcast.info import ChannelStatus
from podcast.info import InfoContent
from podcast.info import PodcastLocation
from podcast.info import RadioStatus
from podcast.models import Channel
from podcast.models import get_channel_id
from podcast.models import get_podcast_id
from podcast.models import Radio
from podcast.models import read_channel_from_id


def build_channel_status(channel: Channel) -> ChannelStatus:
    return ChannelStatus(
        dict(Counter(
            type(podcast.status).__name__
            for podcast in channel.known_podcasts)))


def print_status(radio: Radio) -> typing.Tuple[Radio, InfoContent]:
    radio_status = RadioStatus(dict(
        (get_channel_id(channel), build_channel_status(channel))
        for channel in radio.channels))

    return radio, build_info_content(result=radio_status)


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
            result=PodcastLocation(
                path=download_location(
                    radio.directory,
                    channel,
                    recent_podcast),
                channel_id=channel_id,
                podcast_id=get_podcast_id(recent_podcast),
            ))

    return radio, info_content


def recent_podcast_from_radio(
        radio: Radio,
) -> typing.Tuple[Radio, InfoContent]:
    info_content = build_info_content(error='none found')

    new_podcasts = [
        (channel, podcast)
        for channel in radio.channels
        for podcast in channel.known_podcasts
        if type(podcast.status).__name__ == 'NewStatus'
    ]

    if new_podcasts:
        channel, recent_podcast = sorted(
            new_podcasts,
            key=lambda p: p[1].data.published,
            reverse=True)[0]

        info_content = build_info_content(
            result=PodcastLocation(
                path=download_location(
                    radio.directory,
                    channel,
                    recent_podcast),
                channel_id=get_channel_id(channel),
                podcast_id=get_podcast_id(recent_podcast),
            ))

    return radio, info_content
