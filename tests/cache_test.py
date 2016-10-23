from factory import channel_factory
from podcast.cache import save_known_podcasts
from podcast.cache import load_known_podcasts


TEST_DIR = 'tests/tmp'

# TODO: install and use mock when I'm not on an airplane
def test_smoke():
    channel = channel_factory()
    save_known_podcasts('tmp', channel)
    assert load_known_podcasts('tmp', channel) == channel.known_podcasts