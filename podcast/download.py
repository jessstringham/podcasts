from models import NewPodcast
from feeds import unmerged_podcasts_from_feed


def _download_location(podcast):
    return podcast.podcast_data.audiolink['url'].split('/')[-1].split('.')[-1]

def download_podcast(podcast):
    location = _download_location(podcast)

    return NewPodcast(
        podcast_data=podcast.podcast_data,
        location=location,
    )


def download_channel(channel):
    updated_podcasts = []
    for known_podcast in channel.known_podcast:
        if type(known_podcast).__name__ == 'RequestedPodcast':
            known_podcast = download_podcast(known_podcast)
        updated_podcasts.append(known_podcast)