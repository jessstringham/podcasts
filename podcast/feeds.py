from time import mktime

import feedparser
from models import Podcast
from models import PodcastData
from models import UnmergedStatus


def _find_mp3_link_in_feed_item_links(feed_item_links):
    for item in feed_item_links:
        if item['type'].startswith('audio'):
            return item


def _podcasts_from_feed(url_or_stream):
    return feedparser.parse(url_or_stream)['entries']


def unmerged_podcasts_from_feed(channel):
    feed = _podcasts_from_feed(channel.channel_info.url)
    return [
        Podcast(
            data=PodcastData(
                title=item['title'],
                subtitle=item['subtitle'],
                published=mktime(item['published_parsed']),
                audio_link=_find_mp3_link_in_feed_item_links(item['links'])),
            status=UnmergedStatus())
        for item in feed]
