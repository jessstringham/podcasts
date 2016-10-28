import os
import tempfile

import mock
from util.factory import channel_factory
from util.factory import new_podcast_factory
from util.factory import radio_factory

from podcast.delete import _delete_podcast
from podcast.delete import delete_podcast
from podcast.delete import delete_podcast_from_channel
from podcast.files import download_location
from podcast.files import trash_location
from podcast.models import DeletedStatus
from podcast.models import get_channel_id
from podcast.models import get_podcast_id
from podcast.models import Podcast
from podcast.models import RadioDirectory


def test_missing_file():
    channel = channel_factory()
    fake_podcast = new_podcast_factory()
    with tempfile.TemporaryDirectory() as tmpdirname:
        assert not _delete_podcast(
            RadioDirectory(tmpdirname),
            channel,
            fake_podcast)


def test_move_to_trash():
    channel = channel_factory()
    fake_podcast = new_podcast_factory()

    with tempfile.TemporaryDirectory() as tmpdirname:
        filename = download_location(
            RadioDirectory(tmpdirname),
            channel,
            fake_podcast)

        trash_filename = trash_location(
            RadioDirectory(tmpdirname),
            channel,
            fake_podcast)

        os.makedirs(os.path.dirname(filename))

        open(filename, 'a').close()

        assert os.path.exists(filename)
        assert not os.path.exists(trash_filename)

        assert _delete_podcast(
            RadioDirectory(tmpdirname),
            channel,
            fake_podcast)

        assert not os.path.exists(filename)
        assert os.path.exists(trash_filename)


def test_delete_podcast_from_channel():
    fake_podcast = new_podcast_factory()
    channel = channel_factory(known_podcasts=[fake_podcast])

    podcast_id = get_podcast_id(fake_podcast)

    not_podcast_id = "123"
    assert podcast_id != not_podcast_id

    with mock.patch('podcast.delete._delete_podcast'):
        result = delete_podcast_from_channel(
            RadioDirectory("tmp"), channel, not_podcast_id)

    assert len(result) == 1
    assert result[0] == fake_podcast

    with mock.patch('podcast.delete._delete_podcast'):
        result = delete_podcast_from_channel(
            RadioDirectory("tmp"), channel, podcast_id)

    assert len(result) == 1
    assert result[0] == Podcast(
        status=DeletedStatus(),
        data=fake_podcast.data)


def test_delete_podcast():
    directory = RadioDirectory('tmp')

    channel = channel_factory()
    radio = radio_factory(
        directory=directory,
        channels=[channel],
    )

    channel_id = get_channel_id(channel)
    podcast_id = '123'

    with mock.patch(
            'podcast.delete.delete_podcast_from_channel'
    ) as mock_delete:
        delete_podcast(radio, channel_id, podcast_id)
        mock_delete.mock_calls == [
            mock.call(
                directory,
                channel,
                podcast_id,
            )
        ]
