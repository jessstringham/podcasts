import os
import typing

from podcast.files import download_location
from podcast.files import trash_location
from podcast.models import Channel
from podcast.models import DeletedStatus
from podcast.models import get_channel_id
from podcast.models import get_podcast_id
from podcast.models import Podcast
from podcast.models import Radio
from podcast.models import RadioDirectory


def _delete_podcast(
        directory: RadioDirectory,
        channel: Channel,
        podcast: Podcast,
) -> bool:

    # Where should this file be?
    filename = download_location(
        directory,
        channel,
        podcast)

    # If this file exists, move it to the trash_location
    if os.path.exists(filename):
        trash_filename = trash_location(directory, channel, podcast)

        # First, make sure the trash directory exists
        if not os.path.exists(os.path.dirname(trash_filename)):
            os.makedirs(os.path.dirname(trash_filename))

        os.rename(filename, trash_filename)
        return True

    return False


def delete_podcast_from_channel(
        directory: RadioDirectory,
        channel: Channel,
        podcast_id: str
) -> typing.List[Podcast]:

    updated_podcasts = []
    for podcast in channel.known_podcasts:
        if get_podcast_id(podcast) == podcast_id:
            _delete_podcast(directory, channel, podcast)
            podcast._replace(status=DeletedStatus())
        updated_podcasts.append(podcast)

    return updated_podcasts


def delete_podcast(radio: Radio, channel_id: str, podcast_id: str) -> Radio:
    updated_channels = []
    for channel in radio.channels:
        if get_channel_id(channel) == channel_id:
            channel = channel._replace(
                known_podcasts=delete_podcast_from_channel(
                    radio.directory,
                    channel,
                    podcast_id))
        updated_channels.append(channel)

    return radio._replace(channels=updated_channels)
