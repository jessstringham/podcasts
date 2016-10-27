import podcast.delete
from podcast.delete import _should_really_delete_file
from podcast.delete import _trash_filename
from podcast.models import RadioDirectory

TEST_DIR = 'tests/tmp'


def test_trash_filename():
    expected = 'tmp/.trash/time/yes.mp3'
    actual = _trash_filename(RadioDirectory('tmp'), 'tmp/time/yes.mp3')
    assert expected == actual


def test_should_really_delete_file():
    assert _should_really_delete_file(
        RadioDirectory('tmp'), 'tmp/time/yes.mp3')
    assert not _should_really_delete_file(
        RadioDirectory('tmp'), 'time/yes.mp3')
    assert not _should_really_delete_file(RadioDirectory('tmp'), '/yes.mp3')


def test_wrong_dir(monkeypatch):
    def noop(*args, **kwargs):
        return
    monkeypatch.setattr(podcast.delete, '_throw_in_trash', noop)
