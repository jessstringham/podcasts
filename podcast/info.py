import time
import typing

import simplejson

ChannelStatus = typing.NewType(
    'ChannelStatus',
    typing.Dict[str, int])

RadioStatus = typing.NewType(
    'RadioStatus',
    typing.Dict[str, ChannelStatus])


InfoResult = typing.Union[
    None,
    RadioStatus,
    bool,  # TODO add schemas for these
    typing.Dict[str, str],  # TODO add schemas for these
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
