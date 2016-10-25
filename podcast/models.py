import typing
from collections import namedtuple


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
NewStatus = typing.NamedTuple('NewStatus', [('location', str)])
StartedStatus = typing.NamedTuple('StartedStatus', [('location', str)])
FinishedStatus = typing.NamedTuple('FinishedStatus', [('location', str)])
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

ChannelInfo = namedtuple('ChannelInfo', 'name url directory')

Channel = typing.NamedTuple('Channel', [
    ('channel_info', ChannelInfo),
    ('known_podcasts', typing.List[Podcast])])


def get_channel_label(channel: Channel) -> str:
    return channel.channel_info.name

RadioDirectory = typing.NewType('RadioDirectory', str)


Radio = typing.NamedTuple('Radio', [
    ('channels', typing.List[Channel]),
    ('directory', RadioDirectory)])
