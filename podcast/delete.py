import os
import typing

from podcast.files import download_location
from podcast.files import trash_location
from podcast.info import InfoContent
from podcast.models import Channel
from podcast.models import DeletedStatus
from podcast.models import get_channel_id
from podcast.models import get_podcast_id
from podcast.models import map_channel_podcasts
from podcast.models import map_radio_channels
from podcast.models import Podcast
from podcast.models import Radio
from podcast.models import RadioDirectory


def _delete_podcast_file(
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


def delete_podcast(
        radio: Radio,
        channel_id: str,
        podcast_id: str
) -> typing.Tuple[Radio, InfoContent]:

    def apply_delete_on_right_podcast(
            channel: Channel,
            podcast: Podcast
    ) -> Podcast:
        if get_podcast_id(podcast) == podcast_id:
            _delete_podcast_file(radio.directory, channel, podcast)
            podcast = podcast._replace(status=DeletedStatus())
        return podcast

    def apply_delete_on_right_channel(channel: Channel) -> Channel:
        if get_channel_id(channel) == channel_id:
            channel = map_channel_podcasts(
                channel,
                apply_delete_on_right_podcast)
        return channel

    radio = map_radio_channels(radio, apply_delete_on_right_channel)

    return radio, InfoContent({})
