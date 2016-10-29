import argparse
import typing
from collections import Counter

from podcast.cache import save_radio
from podcast.channel_config import load_channel_config
from podcast.delete import delete_podcast
from podcast.download import download_channel
from podcast.models import blank_info
from podcast.models import Info  # noqa
from podcast.models import InfoContent
from podcast.models import output_info
from podcast.models import Radio
from podcast.models import RadioDirectory
from podcast.update import update_channel


def print_status(radio: Radio) -> typing.Tuple[Radio, InfoContent]:
    status = InfoContent(dict(Counter(
        '{0} -- {1}'.format(channel.channel_info.name,
                            type(podcast.status).__name__)
        for channel in radio.channels
        for podcast in channel.known_podcasts)))

    return radio, status


def load_radio(
        directory: RadioDirectory,
        config: str
) -> Radio:

    return Radio(
        channels=load_channel_config(directory, config),
        directory=RadioDirectory(directory))


def update_radio(radio: Radio) -> typing.Tuple[Radio, InfoContent]:
    updated_channels = [
        update_channel(channel)
        for channel in radio.channels
    ]

    radio = radio._replace(channels=updated_channels)
    info_content = InfoContent({})

    return (radio, info_content)


def download_radio(radio: Radio) -> typing.Tuple[Radio, InfoContent]:
    downloaded_channels = [
        download_channel(radio.directory, channel)
        for channel in radio.channels
    ]

    radio = radio._replace(channels=downloaded_channels)
    info_content = InfoContent({})

    return (radio, info_content)


def save(radio: Radio) -> None:
    save_radio(radio)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loads podcasts.')
    parser.add_argument('command')

    # TODO: these are required options, eeh
    parser.add_argument('--config')
    parser.add_argument('--directory')

    parser.add_argument('--channel-id')
    parser.add_argument('--podcast-id')

    args = parser.parse_args()

    info = blank_info(args.command, args.directory, args.config)

    radio = load_radio(args.directory, args.config)

    radio_action = {
        'status': print_status,
        'update': update_radio,
        'download': download_radio,
    }  # type: typing.Dict[str, typing.Callable[[Radio], typing.Tuple[Radio, InfoContent]]]  # noqa

    if args.command in radio_action:
        radio, info_content = radio_action[args.command](radio)
        info = info._replace(content=info_content)

    podcast_action = {
        'delete': delete_podcast,
    }  # type: typing.Dict[str, typing.Callable[[Radio, str, str], typing.Tuple[Radio, InfoContent]]]  # noqa

    if all([args.podcast_id,
            args.channel_id,
            args.command in podcast_action]):
        radio, info_content = podcast_action[args.command](
            radio, args.channel_id, args.podcast_id)
        info = info._replace(content=info_content)

    save(radio)

    print(output_info(info))
