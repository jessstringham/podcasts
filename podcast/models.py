from collections import namedtuple

Radio = namedtuple('Radio', 'channels directory')
ChannelInfo = namedtuple('ChannelInfo', 'name url directory')
Channel = namedtuple('Channel', 'channel_info known_podcasts')


PodcastData = namedtuple('PodcastData', [
    'title',  # title
    'subtitle',  # subtitle
    'published',  # time published
    'audio_link',  # string of the audio url, or None if we couldn't find one
])


# Podcast states
UnmergedStatus = namedtuple('UnmergedStatus', '')
RequestedStatus = namedtuple('RequestedStatus', '')
CancelledStatus = namedtuple('CancelledStatus', '')
NewStatus = namedtuple('NewStatus', 'location')
StartedStatus = namedtuple('StartedStatus', 'location')
FinishedStatus = namedtuple('FinishedStatus', 'location')
DeletedStatus = namedtuple('DeletedStatus', '')

Podcast = namedtuple('Podcast', 'data status')
