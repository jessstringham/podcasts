import time
import typing

import simplejson


# TODO: add better schemas here
InfoContent = typing.NamedTuple('Info', [
    ('result', typing.Optional[typing.Any]),
    ('error', typing.Optional[str]),
])


def build_info_content(
        result: typing.Optional[typing.Any]=None,
        error: typing.Optional[str]=None) -> InfoContent:
    return InfoContent(
        result=None,
        error=None
    )

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
