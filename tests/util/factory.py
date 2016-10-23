from podcast.models import CancelledPodcast
from podcast.models import Channel
from podcast.models import ChannelInfo
from podcast.models import DeletedPodcast
from podcast.models import FinishedPodcast
from podcast.models import NewPodcast
from podcast.models import PodcastData
from podcast.models import RequestedPodcast
from podcast.models import StartedPodcast
from podcast.models import UnmergedPodcast

DEFAULT_CHANNEL_INFO_NAME = 'test_name'
DEFAULT_CHANNEL_INFO_URL = 'url'
DEFAULT_CHANNEL_INFO_DIRECTORY = 'test_dir'

PODCAST_DATA_TITLE = 'title'
PODCAST_DATA_SUBTITLE = 'subtitle'
PODCAST_DATA_PUBLISHED = 'published'
PODCAST_DATA_AUDIO_LINK = 'audio_link'

DEFAULT_PODCAST_LOCATION = 'location'


def channel_info_factory():
    return ChannelInfo(
        name=DEFAULT_CHANNEL_INFO_NAME,
        url=DEFAULT_CHANNEL_INFO_URL,
        directory=DEFAULT_CHANNEL_INFO_DIRECTORY)


def podcast_data_factory(audio_link=None):
    if audio_link is None:
        audio_link = PODCAST_DATA_AUDIO_LINK
    return PodcastData(
        title=PODCAST_DATA_TITLE,
        subtitle=PODCAST_DATA_SUBTITLE,
        published=PODCAST_DATA_PUBLISHED,
        audio_link=audio_link,
    )


def unmerged_podcast_factory():
    return UnmergedPodcast(
        podcast_data=podcast_data_factory())


def requested_podcast_factory():
    return RequestedPodcast(
        podcast_data=podcast_data_factory())


def cancelled_podcast_factory():
    return CancelledPodcast(
        podcast_data=podcast_data_factory())


def new_podcast_factory():
    return NewPodcast(
        podcast_data=podcast_data_factory(),
        location=DEFAULT_PODCAST_LOCATION)


def started_podcast_factory():
    return StartedPodcast(
        podcast_data=podcast_data_factory(),
        location=DEFAULT_PODCAST_LOCATION)


def finished_podcast_factory():
    return FinishedPodcast(
        podcast_data=podcast_data_factory(),
        location=DEFAULT_PODCAST_LOCATION)


def deleted_podcast_factory():
    return DeletedPodcast(
        podcast_data=podcast_data_factory())


def known_podcasts_factory():
    return [
        unmerged_podcast_factory(),
        requested_podcast_factory(),
        cancelled_podcast_factory(),
        new_podcast_factory(),
        started_podcast_factory(),
        finished_podcast_factory(),
        deleted_podcast_factory(),
    ]


def channel_factory(known_podcasts=None):
    if known_podcasts is None:
        known_podcasts = known_podcasts_factory()

    return Channel(
        channel_info=channel_info_factory(),
        known_podcasts=known_podcasts)
