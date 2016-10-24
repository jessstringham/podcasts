from podcast.feeds import unmerged_podcasts_from_feed
from podcast.models import RequestedStatus


def _uniquer(unmerged_podcast):
    return unmerged_podcast.data.audio_link


def merge_podcasts(channel, unmerged_podcasts):
    known_podcast_audio_links = set(
        _uniquer(podcast)
        for podcast in channel.known_podcasts)

    new_podcasts = []

    for unmerged_podcast in unmerged_podcasts:
        if _uniquer(unmerged_podcast) not in known_podcast_audio_links:
            new_podcasts.append(
                unmerged_podcast._replace(
                    status=RequestedStatus()))
        known_podcast_audio_links.add(_uniquer(unmerged_podcast))

    return new_podcasts


def update_channel(channel):
    unmerged_podcasts = unmerged_podcasts_from_feed(channel)

    return channel._replace(
        known_podcasts=channel.known_podcasts
        + merge_podcasts(channel, unmerged_podcasts))
