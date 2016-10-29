import os
import tempfile

import mock
from util.factory import channel_factory
from util.factory import new_podcast_factory
from util.factory import radio_factory

from podcast.delete import _delete_podcast_file
from podcast.delete import delete_podcast
from podcast.files import download_location
from podcast.files import trash_location
from podcast.models import get_channel_id
from podcast.models import get_podcast_id
from podcast.models import RadioDirectory


def test_missing_file():
    channel = channel_factory()
    new_podcast = new_podcast_factory()
    with tempfile.TemporaryDirectory() as tmpdirname:
        assert not _delete_podcast_file(
            RadioDirectory(tmpdirname),
            channel,
            new_podcast)


def test_move_to_trash():
    channel = channel_factory()
    new_podcast = new_podcast_factory()

    with tempfile.TemporaryDirectory() as tmpdirname:
        filename = download_location(
            RadioDirectory(tmpdirname),
            channel,
            new_podcast)

        trash_filename = trash_location(
            RadioDirectory(tmpdirname),
            channel,
            new_podcast)

        os.makedirs(os.path.dirname(filename))

        open(filename, 'a').close()

        assert os.path.exists(filename)
        assert not os.path.exists(trash_filename)

        assert _delete_podcast_file(
            RadioDirectory(tmpdirname),
            channel,
            new_podcast)

        assert not os.path.exists(filename)
        assert os.path.exists(trash_filename)


def test_delete_podcast_from_channel():
    new_podcast = new_podcast_factory()
    channel = channel_factory(known_podcasts=[new_podcast])
    radio = radio_factory(channels=[channel])

    channel_id = get_channel_id(channel)
    podcast_id = get_podcast_id(new_podcast)

    not_podcast_id = "123"
    assert podcast_id != not_podcast_id

    def first_podcast_on_radio_type(radio):
        assert len(radio.channels) == 1
        assert len(radio.channels[0].known_podcasts) == 1
        return type(radio.channels[0].known_podcasts[0].status).__name__

    with mock.patch('podcast.delete._delete_podcast_file'):
        result, _ = delete_podcast(
            radio, channel_id, not_podcast_id)

    assert first_podcast_on_radio_type(result) == 'NewStatus'

    with mock.patch('podcast.delete._delete_podcast_file'):
        result, _ = delete_podcast(
            radio, channel_id, podcast_id)

    assert first_podcast_on_radio_type(result) == 'DeletedStatus'


def test_delete_podcast():
    directory = RadioDirectory('tmp')

    podcast = new_podcast_factory()
    channel = channel_factory(
        known_podcasts=[podcast]
    )
    radio = radio_factory(
        directory=directory,
        channels=[channel],
    )

    channel_id = get_channel_id(channel)
    podcast_id = get_podcast_id(podcast)

    with mock.patch('podcast.delete._delete_podcast_file') as mock_delete:
        delete_podcast(radio, channel_id, podcast_id)
        mock_delete.mock_calls == [
            mock.call(
                directory,
                channel,
                podcast,
            )
        ]
