import os.path

from podcast.models import Channel
from podcast.models import get_podcast_url
from podcast.models import Podcast
from podcast.models import RadioDirectory


def download_location(
        directory: RadioDirectory,
        channel: Channel,
        podcast: Podcast
) -> str:
    return os.path.join(
        directory,
        channel.channel_info.directory,
        get_podcast_url(podcast))


def trash_location(
        directory: RadioDirectory,
        channel: Channel,
        podcast: Podcast
) -> str:
    return os.path.join(
        directory,
        '.trash',
        channel.channel_info.directory,
        get_podcast_url(podcast))
