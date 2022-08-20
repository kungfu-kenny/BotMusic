# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SearchItem(scrapy.Item):
    name = 'search_item'

class SongItem(scrapy.Item):
    name = 'song_item'

