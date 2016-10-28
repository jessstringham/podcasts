import mock
from util.factory import channel_factory
from util.factory import new_podcast_factory
from util.factory import unmerged_podcast_factory

from podcast.update import merge_podcasts
from podcast.update import update_channel


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
    assert type(podcasts[0].status).__name__ == 'RequestedStatus'


def test_unmerged_podcasts_from_feed():
    channel = channel_factory(known_podcasts=[])
    new_podcast = new_podcast_factory()

    assert channel.known_podcasts == []
    with mock.patch(
            'podcast.update.unmerged_podcasts_from_feed',
            return_value=[new_podcast]):
        channel = update_channel(channel)
    assert channel.known_podcasts == [new_podcast]
