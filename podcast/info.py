import time
import typing

import simplejson


ChannelStatus = typing.NamedTuple(
    'ChannelStatus', [
        # maps a status to number in that status
        ('counts', typing.Dict[str, int]),
        # Long name of the channel
        ('name', str),
    ]
)

RadioStatus = typing.NewType(
    'RadioStatus',
    typing.Dict[str, ChannelStatus])  # maps a station to ChannelStatus

PodcastLocation = typing.NamedTuple('PodcastLocation', [
    ('path', str),
    ('podcast_id', str),
    ('channel_id', str),
])


InfoResult = typing.Union[
    None,
    RadioStatus,
    PodcastLocation,
    bool,  # TODO add schemas for these
]

InfoContent = typing.NamedTuple('Info', [
    ('result', InfoResult),
    ('error', typing.Optional[str]),
])


def build_info_content(
        result: InfoResult=None,
        error: typing.Optional[str]=None) -> InfoContent:
    return InfoContent(
        result=result,
        error=error)

Info = typing.NamedTuple('Info', [
    ('timestamp', float),
    ('command', str),
    ('directory', str),
    ('config_file', str),
    ('content', InfoContent)])


def build_info(args: typing.Any, info_content: InfoContent) -> Info:
    return Info(
        timestamp=time.time(),
        command=args.command,
        directory=args.directory,
        config_file=args.config,
        content=info_content)


def output_info(info: Info) -> str:
    return simplejson.dumps(info._asdict())
