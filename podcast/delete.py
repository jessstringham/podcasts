import os
import typing

from podcast.models import DeletedStatus
from podcast.models import get_podcast_file_location
from podcast.models import get_podcast_id
from podcast.models import Podcast
from podcast.models import Radio
from podcast.models import RadioDirectory


def _trash_filename(directory: RadioDirectory, filename: str) -> str:
    return os.path.join(
        directory,
        '.trash',
        os.path.basename(os.path.dirname(filename)),
        os.path.basename(filename))


def _throw_in_trash(directory: RadioDirectory, filename: str) -> None:
    trash_filename = _trash_filename(directory, filename)

    print("Throwing file:\n  {0}\nin trash\n  {1}".format(
        filename,
        trash_filename))

    if not os.path.exists(os.path.dirname(trash_filename)):
        os.makedirs(os.path.dirname(trash_filename))

    if not os.path.exists(filename):
        print("Didn't delete podcast: file doesn't exist")

    os.rename(filename, trash_filename)


def _should_really_delete_file(
        directory: RadioDirectory,
        filename: str) -> bool:
    return filename.startswith(directory)


def _delete_podcast(directory: RadioDirectory, podcast: Podcast) -> Podcast:
    filename = get_podcast_file_location(podcast)

    # If this podcast isn't deleteable, we're done
    if not filename:
        print("This podcast doesn't need to have a file deleted")
        return podcast._replace(status=DeletedStatus())

    # Deleting files is scary, so let's make sure it's in the
    # folder we were given permission to modify
    if not _should_really_delete_file(directory, filename):
        print("Error deleting podcast: are you changing directories?")
        return podcast

    _throw_in_trash(directory, filename)

    print("Marking podcast as deleted")
    return podcast._replace(status=DeletedStatus())


def delete_podcast_from_list(
        directory: RadioDirectory,
        podcasts: typing.List[Podcast],
        podcast_id: str
) -> typing.List[Podcast]:

    updated_podcasts = []
    for podcast in podcasts:
        if get_podcast_id(podcast) == podcast_id:
            podcast = _delete_podcast(directory, podcast)
        updated_podcasts.append(podcast)

    return updated_podcasts


def delete_podcast(radio: Radio, channel_id: str, podcast_id: str) -> Radio:
    updated_channels = []
    for channel in radio.channels:
        if channel.channel_info.directory == channel_id:
            channel = channel._replace(
                known_podcasts=delete_podcast_from_list(
                    radio.directory,
                    channel.known_podcasts,
                    podcast_id))
        updated_channels.append(channel)

    return radio._replace(channels=updated_channels)
