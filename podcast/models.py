import time
import typing
from collections import namedtuple
from urllib.parse import urlparse

import simplejson


PodcastData = typing.NamedTuple('PodcastData', [
    ('title', str),  # title
    ('subtitle', str),  # subtitle
    ('published', float),  # time published
    # string of the audio url, or None if we couldn't find one
    ('audio_link', typing.Dict[str, str]),
])


# Podcast states
UnmergedStatus = typing.NamedTuple('UnmergedStatus', [])
RequestedStatus = typing.NamedTuple('RequestedStatus', [])
CancelledStatus = typing.NamedTuple('CancelledStatus', [])
NewStatus = typing.NamedTuple('NewStatus', [])
StartedStatus = typing.NamedTuple('StartedStatus', [])
FinishedStatus = typing.NamedTuple('FinishedStatus', [])
DeletedStatus = typing.NamedTuple('DeletedStatus', [])

Podcast = typing.NamedTuple('Podcast', [
    ('data', PodcastData),
    ('status', typing.Union[
        UnmergedStatus,
        RequestedStatus,
        CancelledStatus,
        NewStatus,
        StartedStatus,
        FinishedStatus,
        DeletedStatus,
    ])])


def get_podcast_audio_link(podcast: Podcast) -> str:
    return podcast.data.audio_link['href']


def get_podcast_url(podcast: Podcast) -> str:
    return urlparse(get_podcast_audio_link(podcast)).path.split('/')[-1]

# NOTE: This seems like something I'll probably regret


def get_podcast_id(podcast: Podcast) -> str:
    return '.'.join(get_podcast_url(podcast).split('.')[:-1])


ChannelInfo = namedtuple('ChannelInfo', 'name url directory')

Channel = typing.NamedTuple('Channel', [
    ('channel_info', ChannelInfo),
    ('known_podcasts', typing.List[Podcast])])


def get_channel_id(channel: Channel) -> str:
    return channel.channel_info.directory


RadioDirectory = typing.NewType('RadioDirectory', str)


Radio = typing.NamedTuple('Radio', [
    ('channels', typing.List[Channel]),
    ('directory', RadioDirectory)])

InfoContent = typing.NewType('InfoContent', dict)

Info = typing.NamedTuple('Info', [
    ('timestamp', float),
    ('command', str),
    ('directory', str),
    ('config_file', str),
    ('content', InfoContent)])


def blank_info(args: typing.Any) -> Info:
    return Info(
        timestamp=time.time(),
        command=args.command,
        directory=args.directory,
        config_file=args.config,
        content=InfoContent({'error': 'no content'}))


def output_info(info: Info) -> str:
    return simplejson.dumps(info._asdict())
