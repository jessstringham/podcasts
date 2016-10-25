from util.factory import podcast_data_factory

from podcast.download import _download_location
from podcast.models import Podcast
from podcast.models import RadioDirectory
from podcast.models import RequestedStatus


def test_download_location():
    podcast_data = Podcast(
        status=RequestedStatus(),
        data=podcast_data_factory(
            audio_link={
                'length': u'0',
                'href': u'http://feed.thisamericanlife.org/~r/talpodcast/~5/R0qvREKxypU/597.mp3',  # noqa
                'type': u'audio/mpeg',
                'rel': u'enclosure',
            }))

    assert _download_location(RadioDirectory(
        'dir'), podcast_data) == 'dir/597.mp3'
