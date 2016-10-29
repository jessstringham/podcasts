import typing
import urllib.error
import urllib.request

from podcast.files import download_location
from podcast.info import InfoContent
from podcast.models import Channel
from podcast.models import get_podcast_audio_link
from podcast.models import NewStatus
from podcast.models import Podcast
from podcast.models import Radio
from podcast.models import RadioDirectory


def _download_from_url(url: str, location: str) -> bool:
    try:
        urllib.request.urlretrieve(url, location)
        return True
    except (IOError, urllib.error.ContentTooShortError):
        # If a connection can't be made, IOError is raised
        # If the download gets interrupted (ContentTooShortError), we
        # should try again later

        # TODO: can we tell if it was a bad filename (and should stop
        # requesting it), or internet connectivity (and should tell
        # us), or just a fluke (and should retry)?
        return False


def download_podcast(
        directory: RadioDirectory,
        channel: Channel,
        podcast: Podcast) -> Podcast:
    location = download_location(directory, channel, podcast)
    url = get_podcast_audio_link(podcast)

    # TODO: This takes some time, especially when there are a lot to
    # download. I could have this spawn threads, or add priorities,
    # and so on. For now, since it runs every few hours, and is more
    # of a push than a pull situation for the user, I'm leaving it
    # simple
    success = _download_from_url(url, location)

    if success:
        return podcast._replace(status=NewStatus())
    else:
        return podcast


def download_channel(directory: RadioDirectory, channel: Channel) -> Channel:
    updated_podcasts = []
    for known_podcast in channel.known_podcasts:
        if type(known_podcast.status).__name__ == 'RequestedStatus':
            known_podcast = download_podcast(directory, channel, known_podcast)
        updated_podcasts.append(known_podcast)

    return channel._replace(known_podcasts=updated_podcasts)


def download_radio(radio: Radio) -> typing.Tuple[Radio, InfoContent]:
    downloaded_channels = [
        download_channel(radio.directory, channel)
        for channel in radio.channels
    ]

    radio = radio._replace(channels=downloaded_channels)
    info_content = InfoContent({})

    return (radio, info_content)
