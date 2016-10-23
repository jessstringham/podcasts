import os
import cPickle as pickle


CACHE_LOCATION = '.cache'


def get_cache_location(directory, channel):
    return os.path.join(directory, channel.channel_info.directory, CACHE_LOCATION)


def load_known_podcasts(directory, channel):
    filename = get_cache_location(directory, channel)
    if not os.path.exists(filename):
        return []

    with open(filename) as f:
        cache = pickle.load(f)

    return cache


def save_known_podcasts(directory, channel):
    filename = get_cache_location(directory, channel)

    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    with open(filename, 'w') as f:
        pickle.dump(channel.known_podcasts, f)


def save_radio(directory, radio):
    for channel in radio:
        save_known_podcasts(directory, channel)