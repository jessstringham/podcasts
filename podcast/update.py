import typing

from podcast.feeds import unmerged_podcasts_from_feed
from podcast.models import Channel
from podcast.models import InfoContent
from podcast.models import Podcast
from podcast.models import Radio
from podcast.models import RequestedStatus


def _uniquer(unmerged_podcast: Podcast) -> str:
    return unmerged_podcast.data.audio_link['href']


def merge_podcasts(
        channel: Channel,
        unmerged_podcasts: typing.List[Podcast]) -> typing.List[Podcast]:

    known_podcast_audio_links = set(
        _uniquer(podcast)
        for podcast in channel.known_podcasts)

    new_podcasts = []

    for unmerged_podcast in unmerged_podcasts:
        if _uniquer(unmerged_podcast) not in known_podcast_audio_links:
            new_podcasts.append(
                unmerged_podcast._replace(
                    status=RequestedStatus()))
        known_podcast_audio_links.add(_uniquer(unmerged_podcast))

    return channel.known_podcasts + new_podcasts


def update_channel(channel: Channel) -> Channel:
    unmerged_podcasts = unmerged_podcasts_from_feed(channel)

    return channel._replace(
        known_podcasts=merge_podcasts(channel, unmerged_podcasts))


def update_radio(radio: Radio) -> typing.Tuple[Radio, InfoContent]:
    updated_channels = [
        update_channel(channel)
        for channel in radio.channels
    ]

    radio = radio._replace(channels=updated_channels)
    info_content = InfoContent({})

    return (radio, info_content)
