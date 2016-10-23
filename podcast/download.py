from podcast.models import NewPodcast


def _download_location(podcast):
    # TODO: Use a library here
    return podcast.podcast_data.audio_link['href'].split('/')[-1].split('.')[0]


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
