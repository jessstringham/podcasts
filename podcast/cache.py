import cPickle as pickle
import os


CACHE_LOCATION = '.cache'


def _cache_location(directory, channel_info):
    return os.path.join(
        directory,
        channel_info.directory,
        CACHE_LOCATION)


def load_known_podcasts(directory, channel_info):
    filename = _cache_location(directory, channel_info)
    if not os.path.exists(filename):
        return []

    with open(filename) as f:
        cache = pickle.load(f)

    return cache


def save_known_podcasts(directory, channel):
    filename = _cache_location(directory, channel.channel_info)

    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    with open(filename, 'w') as f:
        pickle.dump(channel.known_podcasts, f)


def save_radio(directory, radio):
    for channel in radio:
        save_known_podcasts(directory, channel)
