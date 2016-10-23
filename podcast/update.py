from feeds import unmerged_podcasts_from_feed
from models import Channel
from models import RequestedPodcast


def _uniquer(unmerged_podcast):
    return unmerged_podcast.podcast_data.audio_link


def merge_podcasts(channel, unmerged_podcasts):
    known_podcast_audio_links = set(
        _uniquer(podcast)
        for podcast in channel.known_podcasts)

    new_podcasts = []

    for unmerged_podcast in unmerged_podcasts:
        if _uniquer(unmerged_podcast) not in known_podcast_audio_links:
            new_podcasts.append(
                RequestedPodcast(podcast_data=unmerged_podcast.podcast_data))
        known_podcast_audio_links.add(_uniquer(unmerged_podcast))

    return new_podcasts


def update_channel(channel):
    unmerged_podcasts = unmerged_podcasts_from_feed(channel)

    return Channel(
        channel_info=channel.channel_info,
        known_podcasts=merge_podcasts(channel, unmerged_podcasts))
