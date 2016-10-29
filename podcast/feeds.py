import typing
from time import mktime

import feedparser

from podcast.models import Channel
from podcast.models import Podcast
from podcast.models import PodcastData
from podcast.models import UnmergedStatus


def _find_mp3_link_in_feed_item_links(
        feed_item_links: typing.List[typing.Dict[str, str]]
) -> typing.Dict[str, str]:
    for item in feed_item_links:
        if item['type'].startswith('audio'):
            return item


def _podcasts_from_feed(
        url_or_stream: typing.Union[str, typing.IO[typing.AnyStr]]
) -> typing.List[dict]:
    return feedparser.parse(url_or_stream)['entries']


def unmerged_podcasts_from_feed(
        channel: Channel,
        limit: int
) -> typing.List[Podcast]:
    feed = _podcasts_from_feed(channel.channel_info.url)
    podcasts = [
        Podcast(
            data=PodcastData(
                title=item['title'],
                subtitle=item['subtitle'],
                published=mktime(item['published_parsed']),
                audio_link=_find_mp3_link_in_feed_item_links(item['links'])),
            status=UnmergedStatus())
        for item in feed]

    return sorted(
        podcasts,
        key=lambda p: p.data.published,
        reverse=True)[:limit]
