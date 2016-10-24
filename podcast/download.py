import os
import urllib
from urlparse import urlparse

from podcast.models import NewStatus


def _download_location(directory, podcast):
    return os.path.join(
        directory,
        urlparse(podcast.data.audio_link['href']).path.split('/')[-1])


def _download_from_url(url, location):
    try:
        urllib.urlretrieve(url, location)
        return True
    except IOError:
        # If a connection can't be made, IOError is raised

        # TODO: can we tell if it was a bad filename (and should stop
        # requesting it), or internet connectivity (and should tell
        # us), or just a fluke (and should retry)?
        return False
    except urllib.error.ContentTooShortError:
        # If the download gets interrupted, we should try again later
        return False


def download_podcast(directory, podcast):
    location = _download_location(directory, podcast)

    # TODO: This takes some time, especially when there are a lot to
    # download. I could have this spawn threads, or add priorities,
    # and so on. For now, since it runs every few hours, and is more
    # of a push than a pull situation for the user, I'm leaving it
    # simple
    success = _download_from_url(podcast.data.audio_link['href'], location)

    if success:
        return podcast._replace(status=NewStatus(location=location))
    else:
        return podcast


def download_channel(directory, channel):
    updated_podcasts = []
    for known_podcast in channel.known_podcast:
        if type(known_podcast.status).__name__ == 'RequestedStatus':
            known_podcast = download_podcast(directory, known_podcast)
        updated_podcasts.append(known_podcast)
