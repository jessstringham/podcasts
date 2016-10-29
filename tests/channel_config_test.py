import typing  # noqa

import pytest
from jsonschema.exceptions import ValidationError

import podcast.cache
from podcast.channel_config import _validate_config
from podcast.channel_config import load_channel_config
from podcast.channel_config import parse_channel_info
from podcast.models import Channel
from podcast.models import ChannelInfo
from podcast.models import RadioDirectory


def test_invalid_config_wrong_type():
    data = 1
    with pytest.raises(ValidationError):
        _validate_config(data)


def test_invalid_config_wrong_content_type():
    data = [1]
    with pytest.raises(ValidationError):
        _validate_config(data)


def test_invalid_config_missing_field():
    data = [{}]  # type: typing.Any
    with pytest.raises(ValidationError):
        _validate_config(data)


def test_invalid_config_field_wrong_type():
    data = [{'name': 1, 'url': '2', 'directory': '3'}]
    with pytest.raises(ValidationError):
        _validate_config(data)


def test_valid_config():
    data = [{
        'name': '1',
        'url': '2',
        'directory': '3',
    }, {
        'name': '2',
        'url': '3',
        'directory': '4',
    }]
    _validate_config(data)


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

    actual = load_channel_config(RadioDirectory(
        'directory'), 'tests/data/test_channel_config')
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
