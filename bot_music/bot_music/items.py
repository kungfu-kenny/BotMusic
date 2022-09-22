# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SongAlbumItem(scrapy.Item):
    name = 'song_album_item'

    number_track = scrapy.Field()
    album_id = scrapy.Field()
    album_title = scrapy.Field()
    artist_id = scrapy.Field()
    artist_name = scrapy.Field()
    
    training = scrapy.Field()


class SongItem(scrapy.Item):
    name = 'song_item'

    duration = scrapy.Field()
    album_id = scrapy.Field()
    album_title = scrapy.Field()
    song_id = scrapy.Field()
    song_title = scrapy.Field()
    artist_id = scrapy.Field()
    artist_name = scrapy.Field()

    training = scrapy.Field()
