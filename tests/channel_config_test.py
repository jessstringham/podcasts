import podcast.cache
from podcast.channel_config import load_channel_config
from podcast.channel_config import parse_channel_info
from podcast.models import Channel
from podcast.models import ChannelInfo


def test_parse_channel_info():
    channel_config = {
        'name': '1',
        'url': '2',
        'directory': '3',
    }
    assert parse_channel_info(channel_config) == ChannelInfo('1', '2', '3')


def test_load_config_smoke_test(monkeypatch):
    def mock_load_known_podcasts(_, __):
        return []

    monkeypatch.setattr(podcast.channel_config,
                        'load_known_podcasts', mock_load_known_podcasts)

    actual = load_channel_config('directory', 'tests/data/test_channel_config')
    expected = [
        Channel(
            ChannelInfo(
                name='podcast_name_1',
                url='podcast_url_1',
                directory='podcast_dir_1'),
            known_podcasts=[]),
        Channel(
            ChannelInfo(
                name='podcast_name_2',
                url='podcast_url_2',
                directory='podcast_dir_2'),
            known_podcasts=[]),
    ]

    assert actual == expected
