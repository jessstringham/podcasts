import typing

from podcast.models import CancelledStatus
from podcast.models import Channel
from podcast.models import ChannelInfo
from podcast.models import DeletedStatus
from podcast.models import FinishedStatus
from podcast.models import NewStatus
from podcast.models import Podcast
from podcast.models import PodcastData
from podcast.models import Radio
from podcast.models import RadioDirectory
from podcast.models import RequestedStatus
from podcast.models import StartedStatus
from podcast.models import UnmergedStatus

DEFAULT_CHANNEL_INFO_NAME = 'test_name'
DEFAULT_CHANNEL_INFO_URL = 'url'
DEFAULT_CHANNEL_INFO_DIRECTORY = 'test_dir'

PODCAST_DATA_TITLE = 'title'
PODCAST_DATA_SUBTITLE = 'subtitle'
PODCAST_DATA_PUBLISHED = 123.0
PODCAST_DATA_AUDIO_LINK = {
    'length': u'0',
    'href': u'http://jessicastringham.com/something.mp3',
    'type': u'audio/mpeg',
    'rel': u'enclosure',
}


def channel_info_factory() -> ChannelInfo:
    return ChannelInfo(
        name=DEFAULT_CHANNEL_INFO_NAME,
        url=DEFAULT_CHANNEL_INFO_URL,
        directory=DEFAULT_CHANNEL_INFO_DIRECTORY)


def podcast_data_factory(
        audio_link: typing.Optional[typing.Dict[str, str]]=None
) -> PodcastData:
    if audio_link is None:
        audio_link = PODCAST_DATA_AUDIO_LINK
    return PodcastData(
        title=PODCAST_DATA_TITLE,
        subtitle=PODCAST_DATA_SUBTITLE,
        published=PODCAST_DATA_PUBLISHED,
        audio_link=audio_link,
    )


def unmerged_podcast_factory() -> Podcast:
    return Podcast(
        status=UnmergedStatus(),
        data=podcast_data_factory())


def requested_podcast_factory() -> Podcast:
    return Podcast(
        status=RequestedStatus(),
        data=podcast_data_factory())


def cancelled_podcast_factory() -> Podcast:
    return Podcast(
        status=CancelledStatus(),
        data=podcast_data_factory())


def new_podcast_factory() -> Podcast:
    return Podcast(
        status=NewStatus(),
        data=podcast_data_factory())


def started_podcast_factory() -> Podcast:
    return Podcast(
        status=StartedStatus(),
        data=podcast_data_factory())


def finished_podcast_factory() -> Podcast:
    return Podcast(
        status=FinishedStatus(),
        data=podcast_data_factory())


def deleted_podcast_factory() -> Podcast:
    return Podcast(
        status=DeletedStatus(),
        data=podcast_data_factory())


def known_podcasts_factory() -> typing.List[Podcast]:
    return [
        unmerged_podcast_factory(),
        requested_podcast_factory(),
        cancelled_podcast_factory(),
        new_podcast_factory(),
        started_podcast_factory(),
        finished_podcast_factory(),
        deleted_podcast_factory(),
    ]


def channel_factory(
        known_podcasts: typing.Optional[typing.List[Podcast]]=None
) -> Channel:
    if known_podcasts is None:
        known_podcasts = known_podcasts_factory()

    return Channel(
        channel_info=channel_info_factory(),
        known_podcasts=known_podcasts)


def radio_factory(
        directory: RadioDirectory=None,
        channels: typing.List[Channel]=None):
    if channels is None:
        channels = [channel_factory()]

    if directory is None:
        directory = RadioDirectory('tmp')

    return Radio(
        directory=directory,
        channels=channels,
    )
