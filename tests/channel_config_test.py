from podcast.channel_config import parse_channel_info
from podcast.channel_config import load_channel_config
from podcast.models import ChannelInfo
from podcast.models import Channel

import podcast.cache


def test_parse_channel_info():
    channel_config = {
        'name': '1',
        'url': '2',
        'directory': '3',
    }
    assert parse_channel_info(channel_config) == ChannelInfo('1', '2', '3')


def test_load_config_smoke_test(monkeypatch):
    def mock_load_known_podcasts(_, __):
        return {}

    monkeypatch.setattr(podcast.channel_config, 'load_known_podcasts', mock_load_known_podcasts)

    actual = load_channel_config('directory', 'tests/data/test_channel_config')
    expected = [
        Channel(ChannelInfo('podcast_name_1', 'podcast_url_1', 'podcast_dir_1'), {}),
        Channel(ChannelInfo('podcast_name_2', 'podcast_url_2', 'podcast_dir_2'), {}),
    ]

    assert actual == expected
