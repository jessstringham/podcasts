import argparse
import typing  # noqa

from podcast.cache import save_radio
from podcast.channel_config import load_radio
from podcast.delete import delete_podcast
from podcast.download import download_radio
from podcast.info import build_info
from podcast.info import InfoContent  # noqa
from podcast.info import output_info
from podcast.models import Radio  # noqa
from podcast.recent import recent_podcast_from_channel
from podcast.status import has_new_podcast_from_channel
from podcast.status import print_status
from podcast.update import update_radio


def main() -> None:
    parser = argparse.ArgumentParser(description='Loads podcasts.')
    parser.add_argument('command')

    # TODO: these are required options, eeh
    parser.add_argument('--config')
    parser.add_argument('--directory')

    parser.add_argument('--channel-id')
    parser.add_argument('--podcast-id')

    args = parser.parse_args()

    radio = load_radio(args.directory, args.config)

    radio_action = {
        'status': print_status,
        'update': update_radio,
        'download': download_radio,
    }  # type: typing.Dict[str, typing.Callable[[Radio], typing.Tuple[Radio, InfoContent]]]  # noqa

    channel_action = {
        'recent': recent_podcast_from_channel,
        'has_new': has_new_podcast_from_channel,
    }  # type: typing.Dict[str, typing.Callable[[Radio, str], typing.Tuple[Radio, InfoContent]]]  # noqa

    podcast_action = {
        'delete': delete_podcast,
    }  # type: typing.Dict[str, typing.Callable[[Radio, str, str], typing.Tuple[Radio, InfoContent]]]  # noqa

    if args.command in radio_action:
        radio, info_content = radio_action[args.command](radio)
    elif all([args.channel_id,
              args.command in channel_action]):
        radio, info_content = channel_action[
            args.command](radio, args.channel_id)
    elif all([args.podcast_id,
              args.channel_id,
              args.command in podcast_action]):
        radio, info_content = podcast_action[args.command](
            radio, args.channel_id, args.podcast_id)
    else:
        info_content = InfoContent({'error': 'command not found'})

    save_radio(radio)

    info = build_info(args, info_content)
    print(output_info(info))

if __name__ == '__main__':
    main()
