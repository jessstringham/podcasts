import time
import typing

import simplejson

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
