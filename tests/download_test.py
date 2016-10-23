from util.factory import podcast_data_factory

from podcast.download import _download_location
from podcast.models import RequestedPodcast


def test_download_location():
    podcast_data = RequestedPodcast(
        podcast_data=podcast_data_factory(
            audio_link={
                'length': u'0',
                'href': u'http://feed.thisamericanlife.org/~r/talpodcast/~5/R0qvREKxypU/597.mp3',  # noqa
                'type': u'audio/mpeg',
                'rel': u'enclosure',
            }
        )
    )

    assert _download_location(podcast_data) == '597'
