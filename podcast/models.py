from collections import namedtuple

ChannelInfo = namedtuple('ChannelInfo', 'name url directory')
Channel = namedtuple('Channel', 'channel_info known_podcasts')


PodcastData = namedtuple('PodcastData', [
    'title',  # title
    'subtitle',  # subtitle
    'published',  # time published
    'audio_link',  # string of the audio url, or None if we couldn't find one
])


# Podcast states
UnmergedPodcast = namedtuple('UnmergedPodcast', 'podcast_data')
RequestedPodcast = namedtuple('RequestedPodcast', 'podcast_data')
CancelledPodcast = namedtuple('CancelledPodcast', 'podcast_data')
NewPodcast = namedtuple('NewPodcast', 'podcast_data location')
StartedPodcast = namedtuple('StartedPodcast', 'podcast_data location')
FinishedPodcast = namedtuple('FinishedPodcast', 'podcast_data location')
DeletedPodcast = namedtuple('DeletedPodcast', 'podcast_data')
