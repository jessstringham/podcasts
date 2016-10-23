from podcast.models import NewStatus
from podcast.models import Podcast


def _download_location(podcast):
    # TODO: Use a library here
    return podcast.data.audio_link['href'].split('/')[-1].split('.')[0]


def download_podcast(podcast):
    location = _download_location(podcast)

    return Podcast(
        status=NewStatus(location=location),
        data=podcast.podcast_data)


def download_channel(channel):
    updated_podcasts = []
    for known_podcast in channel.known_podcast:
        if type(known_podcast.status).__name__ == 'RequestedStatus':
            known_podcast = download_podcast(known_podcast)
        updated_podcasts.append(known_podcast)
