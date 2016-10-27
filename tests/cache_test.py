import tempfile

from util.factory import channel_factory
from util.factory import channel_info_factory
from util.factory import radio_factory

from podcast.cache import load_known_podcasts
from podcast.cache import save_known_podcasts
from podcast.cache import save_radio
from podcast.models import RadioDirectory


def test_read_from_empty_file():
    channel_info = channel_info_factory()

    with tempfile.TemporaryDirectory() as tmpdirname:
        result = load_known_podcasts(RadioDirectory(tmpdirname), channel_info)

    assert result == []


def test_save_to_missing_directory():
    channel = channel_factory()

    with tempfile.TemporaryDirectory() as tmpdirname:
        save_known_podcasts(RadioDirectory(tmpdirname), channel)


def test_smoke():
    channel = channel_factory()

    # Now save some fake data
    with tempfile.TemporaryDirectory() as tmpdirname:
        save_known_podcasts(RadioDirectory(tmpdirname), channel)
        result = load_known_podcasts(
            RadioDirectory(tmpdirname), channel.channel_info)

    # Now, check that loading the channel gives us the expected results

    assert result == channel.known_podcasts


def test_radio():
    with tempfile.TemporaryDirectory() as tmpdirname:
        radio = radio_factory(RadioDirectory(tmpdirname))
        save_radio(radio)
