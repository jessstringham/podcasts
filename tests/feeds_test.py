from factory import channel_factory
from factory import unmerged_podcast_factory

from podcast.feeds import unmerged_podcasts_from_feed
from podcast.feeds import _podcasts_from_feed
import podcast.feeds
from podcast.models import UnmergedPodcast
from podcast.models import PodcastData


def test_smoke(monkeypatch):
    # Create a channel with 3 unmerged podcasts
    channel = channel_factory()

    def mock_podcast_from_feed(_):
        with open('tests/data/test_feed') as f:
            return _podcasts_from_feed(f)

    monkeypatch.setattr(podcast.feeds, '_podcasts_from_feed', mock_podcast_from_feed)

    expected = [
        UnmergedPodcast(
            podcast_data=PodcastData(
                title=u'#502: This Call May Be Recorded... To Save Your Life',
                subtitle=u"A journalist named Meron Estefanos gets a disturbing tip. She's given a phone number that supposedly belongs to a group of refugees being held hostage in the Sinai desert. She dials the number, and soon dozens of strangers are begging her to rescue them.",
                published=1476684000.0,
                audio_link={
                    'length': u'0',
                    'href': u'http://feed.thisamericanlife.org/~r/talpodcast/~5/S12K6GFrc7g/502.mp3',
                    'type': u'audio/mpeg',
                    'rel': u'enclosure'})),
        UnmergedPodcast(
            podcast_data=PodcastData(
                title=u'#598: My Undesirable Talent',
                subtitle=u'San Francisco\u2019s Spider-Man burglar was remarkable. He dropped into buildings from skylights, leapt 10 feet from one roof to another. But mostly, his talent got him into trouble. This week, his story, and stories of other undesirable talents.',
                published=1476079200.0,
                audio_link={'length': u'0', 'href': u'http://feed.thisamericanlife.org/~r/talpodcast/~5/CvhnShvDtl8/598.mp3', 'type': u'audio/mpeg', 'rel': u'enclosure'})),
        UnmergedPodcast(
            podcast_data=PodcastData(
                title=u'#560: Abdi and the Golden Ticket',
                subtitle=u"A story about someone who's desperately trying \u2013 against long odds \u2013 to make it to the United States and become an American. Abdi is a Somali refugee living in Kenya and gets the luckiest break of his life: he wins a lottery that puts him on a short list",
                published=1475474400.0,
                audio_link={'length': u'0', 'href': u'http://feed.thisamericanlife.org/~r/talpodcast/~5/L0ikzBuLkOM/560.mp3', 'type': u'audio/mpeg', 'rel': u'enclosure'})),
        UnmergedPodcast(podcast_data=PodcastData(
            title=u'#597: One Last Thing Before I Go',
            subtitle=u'Words can seem so puny and ineffective sometimes. On this show, we have stories in which ordinary people make last ditch efforts to get through to their loved ones, using a combination of small talk and not-so-small talk.',
            published=1474869600.0,
            audio_link={'length': u'0', 'href': u'http://feed.thisamericanlife.org/~r/talpodcast/~5/R0qvREKxypU/597.mp3', 'type': u'audio/mpeg', 'rel': u'enclosure'}))]

    actual = unmerged_podcasts_from_feed(channel)
    assert actual == expected