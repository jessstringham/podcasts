import argparse
import typing  # noqa

from podcast.cache import save_radio
from podcast.channel_config import load_radio
from podcast.delete import delete_podcast
from podcast.download import download_radio
from podcast.models import blank_info
from podcast.models import InfoContent  # noqa
from podcast.models import output_info
from podcast.models import Radio  # noqa
from podcast.status import print_status
from podcast.update import update_radio


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loads podcasts.')
    parser.add_argument('command')

    # TODO: these are required options, eeh
    parser.add_argument('--config')
    parser.add_argument('--directory')

    parser.add_argument('--channel-id')
    parser.add_argument('--podcast-id')

    args = parser.parse_args()

    info = blank_info(args)

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

    save_radio(radio)

    print(output_info(info))
