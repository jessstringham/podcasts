import typing

from podcast.files import download_location
from podcast.info import InfoContent
from podcast.models import get_channel_id
from podcast.models import get_podcast_id
from podcast.models import Radio


def recent_podcast_from_channel(
        radio: Radio,
        channel_id: str,
) -> typing.Tuple[Radio, InfoContent]:

    info_content = {'error': 'none found'}

    for channel in radio.channels:
        if get_channel_id(channel) == channel_id:
            new_podcasts = filter(
                lambda podcast: type(podcast.status).__name__ == 'NewStatus',
                channel.known_podcasts)

            if new_podcasts:
                recent_podcast = sorted(
                    new_podcasts,
                    key=lambda p: p.data.published,
                    reverse=True)[0]

                info_content = {
                    'path': download_location(
                        radio.directory,
                        channel,
                        recent_podcast),
                    'channel_id': channel_id,
                    'podcast_id': get_podcast_id(recent_podcast),
                }

    return radio, InfoContent(info_content)
