from util.factory import channel_factory

import podcast.feeds
from podcast.feeds import _podcasts_from_feed
from podcast.feeds import unmerged_podcasts_from_feed
from podcast.models import Podcast
from podcast.models import PodcastData
from podcast.models import UnmergedStatus

EXPECTED_FROM_TEST_FEED = [
    Podcast(
        status=UnmergedStatus(),
        data=PodcastData(
            title=u'#502: This Call May Be Recorded... To Save Your Life',
            subtitle=u"A journalist named Meron Estefanos gets a disturbing tip. She's given a phone number that supposedly belongs to a group of refugees being held hostage in the Sinai desert. She dials the number, and soon dozens of strangers are begging her to rescue them.",  # noqa
            published=1476691200.0,
            audio_link={
                'length': u'0',
                'href': u'http://feed.thisamericanlife.org/~r/talpodcast/~5/S12K6GFrc7g/502.mp3',  # noqa
                'type': u'audio/mpeg',
                'rel': u'enclosure'})),
    Podcast(
        status=UnmergedStatus(),
        data=PodcastData(
            title=u'#598: My Undesirable Talent',
            subtitle=u'San Francisco\u2019s Spider-Man burglar was remarkable. He dropped into buildings from skylights, leapt 10 feet from one roof to another. But mostly, his talent got him into trouble. This week, his story, and stories of other undesirable talents.',  # noqa
            published=1476086400.0,
            audio_link={
                'length': u'0',
                'href': u'http://feed.thisamericanlife.org/~r/talpodcast/~5/CvhnShvDtl8/598.mp3',  # noqa
                'type': u'audio/mpeg',
                'rel': u'enclosure'}))]


def test_smoke(monkeypatch):
    # Create a channel with 3 unmerged podcasts
    channel = channel_factory()

    def mock_podcast_from_feed(_):
        with open('tests/data/test_feed', 'rb') as f:
            return _podcasts_from_feed(f)

    monkeypatch.setattr(podcast.feeds, '_podcasts_from_feed',
                        mock_podcast_from_feed)

    actual = unmerged_podcasts_from_feed(channel, 2)
    assert actual == EXPECTED_FROM_TEST_FEED
