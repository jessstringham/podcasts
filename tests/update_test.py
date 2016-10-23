from factory import channel_factory
from factory import unmerged_podcast_factory

import podcast.update
from podcast.update import merge_podcasts

def test_merge_podcast():
    # Create a channel with 3 unmerged podcasts
    channel = channel_factory(known_podcasts=[])

    unmerged_podcasts = [
        unmerged_podcast_factory(),
        unmerged_podcast_factory(),
        unmerged_podcast_factory(),
    ]

    podcasts = merge_podcasts(channel, unmerged_podcasts)

    assert len(podcasts) == 1
    assert type(podcasts[0]).__name__ == 'RequestedPodcast'