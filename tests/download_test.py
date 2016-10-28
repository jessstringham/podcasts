import mock
from util.factory import channel_factory
from util.factory import new_podcast_factory
from util.factory import requested_podcast_factory

from podcast.download import _download_from_url
from podcast.download import download_channel
from podcast.models import NewStatus
from podcast.models import RadioDirectory


def get_types(channel):
    return [
        type(podcast.status).__name__
        for podcast in channel.known_podcasts
    ]


def test_download_channel_none_requested():
    channel = channel_factory(known_podcasts=[
        new_podcast_factory(),
        new_podcast_factory(),
        new_podcast_factory(),
    ])

    with mock.patch(
            'podcast.download.download_podcast') as mock_download_podcast:
        new_channel = download_channel(
            RadioDirectory('tmp'),
            channel)

        assert len(mock_download_podcast.mock_calls) == 0

    assert channel == new_channel
    assert get_types(channel) == get_types(new_channel)


def test_download_channel_success():
    channel = channel_factory(known_podcasts=[requested_podcast_factory()])

    with mock.patch(
            'podcast.download._download_from_url',
            return_value=True) as mock_download_podcast:
        new_channel = download_channel(
            RadioDirectory('tmp'),
            channel)
        assert len(mock_download_podcast.mock_calls) == 1

    expected = channel._replace(
        known_podcasts=[
            channel.known_podcasts[0]._replace(status=NewStatus())
        ])

    assert channel == expected
    assert get_types(new_channel) == get_types(expected)

    # Let's test the tests
    assert get_types(new_channel) != get_types(channel)


def test_download_channel_fail():
    channel = channel_factory(known_podcasts=[requested_podcast_factory()])

    with mock.patch(
            'podcast.download._download_from_url',
            return_value=False) as mock_download_podcast:
        new_channel = download_channel(
            RadioDirectory('tmp'),
            channel)
        assert len(mock_download_podcast.mock_calls) == 1

    assert channel == new_channel
    assert get_types(channel) == get_types(new_channel)


def test_download_from_url_success():
    with mock.patch('urllib.request.urlretrieve'):
        assert _download_from_url(
            'http://jessicastringham.com/something',
            'nope')


def test_download_from_url_fail():
    with mock.patch('urllib.request.urlretrieve', side_effect=IOError):
        assert not _download_from_url(
            'http://jessicastringham.com/something',
            'nope')
