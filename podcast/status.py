import typing
from collections import Counter

from podcast.models import InfoContent
from podcast.models import Radio


def print_status(radio: Radio) -> typing.Tuple[Radio, InfoContent]:
    status = InfoContent(dict(Counter(
        '{0} -- {1}'.format(channel.channel_info.name,
                            type(podcast.status).__name__)
        for channel in radio.channels
        for podcast in channel.known_podcasts)))

    return radio, status
